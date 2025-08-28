import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship, sessionmaker, validates
from sqlalchemy.ext.hybrid import hybrid_property

from .database import Base, engine, Session

#gets the current time(UTC+3 timezone)
EAT_TIMEZONE = timezone(timedelta(hours=3))
def get_current_time_eat():
    """Returns the current time as a timezone-aware datetime object for UTC+3."""
    return datetime.datetime.now(EAT_TIMEZONE)

class Profile(Base):
  """
  Represents a 'scrubbing profile' which is a saved set of metadata tags to be removed.
  This class maps to the 'profiles' table in the database.
  """
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    #Relationships
    #one-to-many relationship between Profile and ProfileTag.
    tags_to_remove = relationship('ProfileTag', back_populates='profile', cascade="all, delete-orphan")
    logs = relationship('FileLog', back_populates='profile_used')

    @hybrid_property
    def name_length(self):
      """A hybrid property that returns the length of the profile's name."""
        return len(self.name)

    @validates('name')
    def validate_name(self, key, name_value):
      """Ensures the profile name is at least 3 characters long."""
        if not name_value or len(name_value) < 3:
            raise ValueError("Profile name must be at least 3 characters long.")
        return name_value

    def __repr__(self):
        return f"<Profile(id={self.id}, name='{self.name}')>"

    
    @classmethod
    def create(cls, session, name, description, tags_list):
      """A class method to create a new Profile, including its tags."""
        #Checks for duplicate profile names
        if session.query(cls).filter_by(name=name).first():
            raise ValueError(f"Profile with name '{name}' already exists.")
        
        profile = cls(name=name, description=description)
        for tag_name in tags_list:
          #Creates and associates ProfileTag objects with the Profile
            profile.tags_to_remove.append(ProfileTag(tag_name=tag_name))
        
        session.add(profile)
        session.commit()
        return profile

    @classmethod
    def get_all(cls, session):
      """A class method to retrieve all profiles from the database."""
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, profile_id):
      """A class method to find a profile by its ID."""
        return session.query(cls).get(profile_id)
    
    @classmethod
    def find_by_name(cls, session, name):
      """A class method to find a profile by its name."""
        return session.query(cls).filter_by(name=name).first()

    def delete(self, session):
      """method to delete this specific profile object from the database."""
        session.delete(self)
        session.commit()

class ProfileTag(Base):
   """
    Represents a single tag name associated with a Profile.
    This is essentially a join table for the many-to-many relationship.
    """
    __tablename__ = 'profile_tags'

    id = Column(Integer, primary_key=True)
    tag_name = Column(String, nullable=False)
    profile_id = Column(Integer, ForeignKey('profiles.id'))

    #Relationships
    profile = relationship('Profile', back_populates='tags_to_remove')

    def __repr__(self):
        return f"<ProfileTag(tag_name='{self.tag_name}')>"
    
  class FileLog(Base):
    """Represents a log entry for a file that has been processed."""
    __tablename__ = 'file_logs'

    id = Column(Integer, primary_key=True)
    original_filepath = Column(String, nullable=False)
    processed_filepath = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=get_current_time_eat)
    profile_used_id = Column(Integer, ForeignKey('profiles.id'), nullable=True)

    #Relationships
    scrubbed_tags = relationship('ScrubbedTag', back_populates='file_log', cascade="all, delete-orphan")
    profile_used = relationship('Profile', back_populates='logs')

    def __repr__(self):
        return f"<FileLog(id={self.id}, original='{self.original_filepath}', time='{self.timestamp}')>"

    @classmethod
    def create(cls, session, original_path, processed_path, scrubbed_tags_dict, profile_id=None):
        """A class method to create a new FileLog and its associated ScrubbedTags."""
        log = cls(
            original_filepath=original_path,
            processed_filepath=processed_path,
            profile_used_id=profile_id
        )
        for tag_name, tag_value in scrubbed_tags_dict.items():
            log.scrubbed_tags.append(ScrubbedTag(tag_name=str(tag_name), tag_value=str(tag_value)))
        
        session.add(log)
        session.commit()
        return log

    @classmethod
    def get_all(cls, session):
        """A class method to retrieve all logs, ordered from newest to oldest."""
        return session.query(cls).order_by(cls.timestamp.desc()).all()

    @classmethod
    def find_by_id(cls, session, log_id):
        """A class method to find a single log by its primary key (id)."""
        return session.query(cls).get(log_id)
        
    def delete(self, session):
        """An instance method to delete this specific log object from the database."""
        session.delete(self)
        session.commit()

