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

    # Relationship
    profile = relationship('Profile', back_populates='tags_to_remove')

    def __repr__(self):
        return f"<ProfileTag(tag_name='{self.tag_name}')>"
