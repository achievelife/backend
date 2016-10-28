# achievelife/backend
The backend for achievelife

# Endpoints
All endpoints require a POST request with specific data.

## API v1
All endpoints EXCEPT for /api/v1/login require the session key to be sent apart of the request.

### /api/v1/login
**INPUT**: user, pass

**OUTPUT**: message, code, session

Logs in a user.  Code will be 200 if the login was successful.  ENSURE YOU KEEP THE SESSION KEY RETURNED.  THIS WILL AUTHENTICATE THE USER FOR ANY OTHER REQUESTS.

### /api/v1/logout
**INPUT**: session

**OUTPUT**: message, code

Terminates a session, if it exists.  Code will be 200 upon success.

### /api/v1/ping
**INPUT**: session

**OUTPUT**: message, code, now

Simple test to see if a session is still active.  Code will be 200 upon success, along with "now" containing the current time.

### /api/v1/getUser
**INPUT**: session

**OUTPUT**: message, code, uid, username

Returns information about the currently logged in user.

### /api/v1/friends
**INPUT**: session

**OUTPUT**: message, code, friends

Returns all friends of the current user.

### /api/v1/nearby
**INPUT**: session

**OUTPUT**: message, code, nearby

Returns nearby activities.

### /api/v1/activity/history
**INPUT**: session

**OUTPUT**: message, code, activities

Returns the entire activity history for the currently logged in user.

### /api/v1/activity/complete
**INPUT**: session

**OUTPUT**: message, code

Complete's an activity.

### /api/v1/activity/start
**INPUT**: session

**OUTPUT**: message, code

Start's an activity.

### /api/v1/activity/end
**INPUT**: session

**OUTPUT**: message, code

End's an activity.

## Admin v1
All endpoints require the admin key to be sent, in order to authenticate the request.

### /admin/v1/getUsers
**INPUT**: key

**OUTPUT**: message, code, users, count

Returns all the users (uid, name) as well as a count of the users

### /admin/v1/getUser
**INPUT**: key, uid

**OUTPUT**: message, code, id, username, level, {skills}, xp

Returns specific information about the user you are requesting information about