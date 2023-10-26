from fastapi import APIRouter, Depends, HTTPException, Form, Response
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from jose import jwt, JWTError
import logging
from datetime import date
from . import sessionController  # Import your session controller module
from db.db import get_db_session, User, Gear # Import your SQLAlchemy User modelfrom db.db import get_db_session, User, AccessToken
from urllib.parse import unquote

# Create an instance of an APIRouter
router = APIRouter()

logger = logging.getLogger("myLogger")

class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    email: str
    city: Optional[str]
    birthdate: Optional[date]
    preferred_language: str
    gender: int
    access_type: int
    photo_path: Optional[str]
    photo_path_aux: Optional[str]
    is_active: int
    strava_token: Optional[str]
    strava_refresh_token: Optional[str]
    strava_token_expires_at: Optional[str]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define an HTTP GET route to retrieve all users
@router.get("/users/all", response_model=list[dict])
async def read_users_all(token: str = Depends(oauth2_scheme)):
    try:
        # Validate the user's access token using the oauth2_scheme
        sessionController.validate_token(token)

        # Validate that the user has admin access
        sessionController.validate_admin_access(token)

        # Create a database session using the get_db_session context manager
        with get_db_session() as db_session: 
           # Query all users from the database
            users = db_session.query(User).all()

            # Convert the SQLAlchemy User objects to dictionaries
            results = [user.to_dict() for user in users]
    except JWTError:
        # Handle JWT (JSON Web Token) authentication error
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Return the list of user dictionaries as the response
    return results

# Define an HTTP GET route to retrieve the number of users
@router.get("/users/number")
async def read_users_number(token: str = Depends(oauth2_scheme)):
    try:
        # Validate the user's access token using the oauth2_scheme
        sessionController.validate_token(token)

        # Validate that the user has admin access
        sessionController.validate_admin_access(token)

        # Create a database session using the get_db_session context manager
        with get_db_session() as db_session:
            # Count the number of users in the database
            user_count = db_session.query(User).count()
    except JWTError:
        # Handle JWT (JSON Web Token) authentication error
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Return the user count as a JSON response
    return {0: user_count}

# Define an HTTP GET route to retrieve user records with pagination
@router.get("/users/all/pagenumber/{pageNumber}/numRecords/{numRecords}", response_model=List[dict])
async def read_users_all_pagination(
    pageNumber: int,
    numRecords: int,
    token: str = Depends(oauth2_scheme)
):
    try:
        # Validate the user's access token using the oauth2_scheme
        sessionController.validate_token(token)

        # Validate that the user has admin access
        sessionController.validate_admin_access(token)

        # Create a database session using the get_db_session context manager
        with get_db_session() as db_session:
            # Use SQLAlchemy to query the user records with pagination
            user_records = (
                db_session.query(User)
                .order_by(User.name.asc())
                .offset((pageNumber - 1) * numRecords)
                .limit(numRecords)
                .all()
            )

            # Convert the SQLAlchemy results to a list of dictionaries
            results = [record.__dict__ for record in user_records]

    except JWTError:
        # Handle JWT (JSON Web Token) authentication error
        raise HTTPException(status_code=401, detail="Unauthorized")
    except Error as err:
        # Handle any other SQLAlchemy or database errors
        print(err)

    # Return the list of user records as a JSON response
    return results

# Define an HTTP GET route to retrieve user records by username
@router.get("/users/userfromusername/{username}", response_model=List[dict])
async def read_users_userFromUsername(username: str, token: str = Depends(oauth2_scheme)):
    try:
        # Validate the user's access token using the oauth2_scheme
        sessionController.validate_token(token)

        # Validate that the user has admin access
        sessionController.validate_admin_access(token)

        # Create a database session using the get_db_session context manager
        with get_db_session() as db_session:
            # Use SQLAlchemy to query the user records by username
            user_records = (
                db_session.query(User)
                .filter(User.username == unquote(username).replace("+", " "))
                .all()
            )

            # Convert the SQLAlchemy results to a list of dictionaries
            results = [record.__dict__ for record in user_records]

    except JWTError:
        # Handle JWT (JSON Web Token) authentication error
        raise HTTPException(status_code=401, detail="Unauthorized")
    except Error as err:
        # Handle any other SQLAlchemy or database errors
        print(err)

    # Return the list of user records as a JSON response
    return results

# Define an HTTP GET route to retrieve user records by user ID
@router.get("/users/userfromid/{user_id}", response_model=List[dict])
async def read_users_userFromId(user_id: int, token: str = Depends(oauth2_scheme)):
    try:
        # Validate the user's access token using the oauth2_scheme
        sessionController.validate_token(token)

        # Validate that the user has admin access
        sessionController.validate_admin_access(token)

        # Create a database session using the get_db_session context manager
        with get_db_session() as db_session:
            # Use SQLAlchemy to query the user records by user ID
            user_records = (
                db_session.query(User)
                .filter(User.id == user_id)
                .all()
            )

            # Convert the SQLAlchemy results to a list of dictionaries
            results = [record.__dict__ for record in user_records]

    except JWTError:
        # Handle JWT (JSON Web Token) authentication error
        raise HTTPException(status_code=401, detail="Unauthorized")
    except Error as err:
        # Handle any other SQLAlchemy or database errors
        print(err)

    # Return the list of user records as a JSON response
    return results

# Define an HTTP GET route to retrieve user ID by username
@router.get("/users/useridfromusername/{username}")
async def read_users_userIDFromUsername(username: str, token: str = Depends(oauth2_scheme)):
    try:
        # Validate the user's access token using the oauth2_scheme
        sessionController.validate_token(token)

        # Validate that the user has admin access
        sessionController.validate_admin_access(token)

        # Create a database session using the get_db_session context manager
        with get_db_session() as db_session:
            # Use SQLAlchemy to query the user ID by username
            user_id = db_session.query(User.id).filter(User.username == unquote(username).replace("+", " ")).first()
    except JWTError:
        # Handle JWT (JSON Web Token) authentication error
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Return the user ID as a JSON response
    return {0: user_id}

# Define an HTTP GET route to retrieve user photos by user ID
@router.get("/users/userphotofromid/{user_id}")
async def read_users_userPhotoFromID(user_id: int, token: str = Depends(oauth2_scheme)):
    try:
        # Validate the user's access token using the oauth2_scheme
        sessionController.validate_token(token)

        # Validate that the user has admin access
        sessionController.validate_admin_access(token)

        # Create a database session using the get_db_session context manager
        with get_db_session() as db_session:
            # Use SQLAlchemy to query the user's photo path by user ID
            user = db_session.query(User.photo_path).filter(User.id == user_id).first()

            if user:
                # Extract the photo_path attribute from the user object
                photo_path = user.photo_path
            else:
                # Handle the case where the user was not found or doesn't have a photo path
                raise HTTPException(status_code=404, detail="User not found or no photo path available")

    except JWTError:
        # Handle JWT (JSON Web Token) authentication error
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Return the user's photo path as a JSON response
    return {0: photo_path}
    

# Define an HTTP GET route to retrieve user photos aux by user ID
@router.get("/users/userphotoauxfromid/{user_id}")
async def read_users_userPhotoAuxFromID(user_id: int, token: str = Depends(oauth2_scheme)):
    try:
        # Validate the user's access token using the oauth2_scheme
        sessionController.validate_token(token)

        # Validate that the user has admin access
        sessionController.validate_admin_access(token)

        # Create a database session using the get_db_session context manager
        with get_db_session() as db_session:
            # Use SQLAlchemy to query the user's photo path by user ID
            user = db_session.query(User.photo_path_aux).filter(User.id == user_id).first()

            if user:
                # Extract the photo_path_aux attribute from the user object
                photo_path_aux = user.photo_path_aux
            else:
                # Handle the case where the user was not found or doesn't have a photo path
                raise HTTPException(status_code=404, detail="User not found or no photo path available")

    except JWTError:
        # Handle JWT (JSON Web Token) authentication error
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Return the user's photo path as a JSON response
    return {0: photo_path_aux}

# Define an HTTP POST route to create a new user
@router.post("/users/create")
async def create_user(
    name: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    preferred_language: str = Form(...),
    city: Optional[str] = Form(None),
    birthdate: Optional[str] = Form(None),
    gender: int = Form(...),
    access_type: int = Form(...),
    photo_path: Optional[str] = Form(None),
    photo_path_aux: Optional[str] = Form(None),
    is_active: int = Form(...),
    token: str = Depends(oauth2_scheme)
):
    try:
        # Validate the user's access token using the oauth2_scheme
        sessionController.validate_token(token)

        # Validate that the user has admin access
        sessionController.validate_admin_access(token)

        # Create a new User instance using SQLAlchemy's ORM
        new_user = User(
            name=name,
            username=username,
            email=email,
            password=password,
            preferred_language=preferred_language,
            city=city,
            birthdate=birthdate,
            gender=gender,
            access_type=access_type,
            photo_path=photo_path,
            photo_path_aux=photo_path_aux,
            is_active=is_active
        )

        with get_db_session() as db_session:
            # Add the new user to the database
            db_session.add(new_user)
            db_session.commit()

        return {"message": "User added successfully"}
    except Error as err:
        # Handle any database-related errors
        print(err)
        raise HTTPException(status_code=500, detail="Internal server error")

# Define an HTTP PUT route to edit a user's information
@router.put("/users/edit/{user_id}")
async def edit_user(
    user_id: int,
    name: str = Form(None),
    username: str = Form(None),
    email: str = Form(None),
    preferred_language: str = Form(None),
    city: Optional[str] = Form(None),
    birthdate: Optional[str] = Form(None),
    gender: int = Form(None),
    access_type: int = Form(None),
    photo_path: Optional[str] = Form(None),
    photo_path_aux: Optional[str] = Form(None),
    is_active: int = Form(None),
    token: str = Depends(oauth2_scheme)
):
    try:
        # Validate the user's access token using the oauth2_scheme
        sessionController.validate_token(token)

        # Validate that the user has admin access
        sessionController.validate_admin_access(token)

        with get_db_session() as db_session:
            # Query the database to find the user by their ID
            user = db_session.query(User).filter(User.id == user_id).first()
            
            # Check if the user with the given ID exists
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Update user information if provided in the form data
            if name is not None:
                user.name = name
            if username is not None:
                user.username = username
            if email is not None:
                user.email = email
            if preferred_language is not None:
                user.preferred_language = preferred_language
            if city is not None:
                user.city = city
            if birthdate is not None:
                user.birthdate = birthdate
            if gender is not None:
                user.gender = gender
            if access_type is not None:
                user.access_type = access_type
            if photo_path is not None:
                user.photo_path = photo_path
            if photo_path_aux is not None:
                user.photo_path_aux = photo_path_aux
            if is_active is not None:
                user.is_active = is_active

            # Commit the changes to the database
            db_session.commit()
    except JWTError:
        # Handle JWT (JSON Web Token) authentication error
        raise HTTPException(status_code=401, detail="Unauthorized")
    except Exception as err:
        # Handle any other unexpected exceptions
        print(err)
        raise HTTPException(status_code=500, detail="Failed to edit user")

    return {"message": "User edited successfully"}

# Define an HTTP PUT route to delete a user's photo
@router.put("/users/{user_id}/delete-photo")
async def delete_user_photo(user_id: int, token: str = Depends(oauth2_scheme)):
    try:
        # Validate the user's access token using the oauth2_scheme
        sessionController.validate_token(token)

        # Validate that the user has admin access
        sessionController.validate_admin_access(token)

        with get_db_session() as db_session:
            # Query the database to find the user by their ID
            user = db_session.query(User).filter(User.id == user_id).first()
            
            # Check if the user with the given ID exists
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Set the user's photo paths to None to delete the photo
            user.photo_path = None
            user.photo_path_aux = None

            # Commit the changes to the database
            db_session.commit()
    except JWTError:
        # Handle JWT (JSON Web Token) authentication error
        raise HTTPException(status_code=401, detail="Unauthorized")
    except Exception as err:
        # Handle any other unexpected exceptions
        print(err)
        raise HTTPException(status_code=500, detail="Failed to update user photo")

    # Return a success message
    return {"message": f"Photo for user {user_id} has been deleted"}

# Define an HTTP DELETE route to delete a user
@router.delete("/users/{user_id}/delete")
async def delete_user(user_id: int, response: Response, token: str = Depends(oauth2_scheme)):
    try:
        # Validate the user's access token using the oauth2_scheme
        sessionController.validate_token(token)

        # Validate that the user has admin access
        sessionController.validate_admin_access(token)

        with get_db_session() as db_session:
            user = db_session.query(User).filter(User.id == user_id).first()
            
            # Check if the user with the given ID exists
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Check for existing dependencies if needed (e.g., related systems)
            count_gear = db_session.query(Gear).filter(gear.user_id == user_id).count()
            if count_gear > 0:
                raise HTTPException(status_code=409, detail="Cannot delete user due to existing dependencies")

            # Delete the user from the database
            db_session.delete(user)
            db_session.commit()
    except JWTError:
        raise HTTPException(status_code=401, detail="Unauthorized")
    except Exception as err:
        raise HTTPException(status_code=500, detail="Failed to delete user")

    # Return a success message upon successful deletion
    return {"message": f"User {user_id} has been deleted"}
