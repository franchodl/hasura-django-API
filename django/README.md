## Django Directory Layout

    ./django/app/

Contains our project settings > contains `settings.py`. The `urls.py` for the root of our project direct us to the `api` application.

    ./django/users/

Contains all of our application logic:

- admin.py
    - What shows up in the Django admin interface (currently disabled, but configured to show any custom info for users)
- apps.py
    - General configuration options
- models.py
    - Extends user model
- auth.py
    - Auth specific views and serializers.
    - Customizes Hasura JWT claims.
- sample_logic.py
    - Contains any extended logic (this is where you can write custom functions).
- sample_email.py
    - Email-specific extended logic
    - This is used below for our email eventing examples, and a custom action example where Hasura -> <- from Django.
- urls.py
    - Routing for API endpoints


## Django Auth Endpoints

**As of 2.0 these are mapped to GraphQL nodes using Hasura Actions.**

## Register User
```
http://localhost:8000/users/user/register/
```
`POST` : accepts `username`, `email`, and `password`. Returns new user info and a first set of returned tokens.

**GQL Query:**
```graphql
mutation userRegister($email: String = "", $password: String = "", $username: String = "") {
  user_register(arg: {password: $password, username: $username, email: $email}) {
    id
    username
    email
    tokens
  }
}
```
**Variable:**
```json
{
  "email": "[EMAIL]",
  "password": "[PASSWORD]",
  "username": "[USERNAME]"
}
```

## Login
```
http://localhost:8000/users/login/
```
`POST` : accepts `username` and `password`. Returns access and refresh tokens.

**GQL Query:**
```graphql
query userLogin($username: String = "", $password: String = "") {
  user_login(arg: {username: $username, password: $password}) {
    access
    refresh
  }
}
```
**Variable:**
```json
{
  "username": "[USERNAME]",
  "password": "[PASSWORD]"
}
```

## Refresh Access Token
```
http://localhost:8000/users/token/refresh/
```
`POST` : accepts `refresh` token. Provides new access token.

**GQL Query:**
```graphql
query userRefresh($refresh: String = "") {
  user_refresh(arg: {refresh: $refresh}) {
    access
  }
}
```
**Variable:**
```json
{
  "refresh": "[REFRESH TOKEN]"
}
```

## Change Password
```
http://localhost:8000/users/user/change_password/
```
`PUT` / `PATCH` : accepts `old_password`, `new_password`. Requires `authorization` header with access token.

**GQL Query:**
```graphql
mutation userChangePassword($old_password: String = "", $new_password: String = "") {
  user_change_password(arg: {old_password: $old_password, new_password: $new_password}) {
    status
    code
  }
}
```
**Variable:**
```json
{
  "old_password": "[OLD PASSWORD]",
  "new_password": "[NEW PASSWORD]"
}
```

## Password Reset (w/ Email Logic)
```
http://localhost:8000/users/reset_password/
```
`POST` : accepts `email`. Generates a password reset token in the database 

*Note: there's a message below in **Events** in where you can add your SMTP email logic logic.*

**GQL Query:**
```graphql
mutation userPasswordReset($email: String = "") {
  user_password_reset(arg: {email: $email}) {
    status
  }
}
```
**Variable:**
```json
{
  "email": "[EMAIL]"
}
```

## Validate Password Reset Token
```
http://localhost:8000/users/reset_password/validate_token/
```
`POST` : accepts `email` and `token`. Returns 200 OK status if the token is verified.

**GQL Query:**
```graphql
query userPasswordResetValidateToken($email: String = "", $token: String = "") {
  user_password_reset_validate(arg: {email: $email, token: $token}) {
    status
  }
}
```
**Variable:**
```json
{
  "email": "[EMAIL]",
  "token": "[TOKEN]"
}
```

## Confirm and Submit Password Reset
```
http://localhost:8000/users/reset_password/confirm/
```
`POST` : accepts `email`, `token`, `password` (new password). Returns 200 status if the token + email pair is verified and the password is updated.

**GQL Query:**
```graphql
mutation userPasswordResetChangeConfirm($email: String = "", $token: String = "", $password: String = "") {
  user_password_reset_confirm(arg: {email: $email, token: $token, password: $password}) {
    status
  }
}
```
**Variable:**
```json
{
  "email": "[EMAIL]",
  "password": "[PASSWORD]",
  "token": "[TOKEN]"
}
```

-----

Aside from the data views Hasura provides through GraphQL from our database's tables, how else can we get views of our data?


## Using Hasura + Django to Handle Advanced Business Logic (Python)
This project makes use of 2 of Hasura's methods for extending it's generate CRUD API.

### Events
- Events use database eventing to provide *at least once* delivery of a database event (create, update, etc.) to a webhook endpoint.
- We have 2 custom events created at `http://localhost:8080/console/events/data/manage` for sending emails to newly registered users and new password resets.
    - These events throw to endpoints which are defined at `./django/users/sample_emails.py` (+ `./django/users/urls.py`).
    - You'll notice each of these items have a flag to define completion (`registration_sent`, and `reset_sent` in their respective tables) - that's because of the at least once caveat to make sure that in the case of a double-send (rare, but happens), we don't accidentally double-send an email.

### Actions
- Actions extend the query or mutation root of the generated API to define a payload which will be sent to a webhook endpoint, and an expected response to get back.
- We have 1 action created at `http://localhost:8080/console/actions/manage/actions` which is a very simple example.
    - The payload is a food which will be thrown to the logic defined in `./django/users/sample_logic.py` (+ `./django/users/urls.py`).
    - The logic looks at if the food entered is a hotdog and replies *true* of *false*.
    - The nice part of this we can lean on Django's built in `@permission_classes([IsAuthenticated])` decorator in `sample_logic.py` to verify I'm a logged in user making the request (we're passing our headers from the action), and pair that with Hasura's permissions around which role should be able to make the request through GraphQL.


## JWT Handling
We've made a couple of small changes to how we handle JWT tokens vs the standard SimpleJWT implementation. 

There are typically 2 gotchas when handling tokens:

- How can I revoke a token (instances of deactivating accounts)?
- Is the current token's claims valid?

The way we've looked to solve these issues are:

- Short access token life, longer refresh token (standard) - this can be set through settings in `./django/app/settings.py`
- Instead of blacklisting tokens (which is one way to revoke tokens), on refresh we check for:
    - Whether the user exists / is marked as active in the DB.
    - Whether the JWT claims for the user's role match the `user.profile.role` which is set in the DB.
        - If either of these throw an exception, refresh endpoint will reply with a 401 (and the user should be redirected to login and obtain a new access / refresh token pair if their account is valid).

You can find, change, or disable all of this logic in `./django/users/auth.py`


## Setting Up Emails (and the Reset Password Flow)
We have some sample email logic which can be found in `./django/users/sample_emails.py` which can be uncommented and used as needed.

For the reset password flow, generally you'll be looking to handle the token as:
- Embed token in URL link in email (boilerplate shows one implementation of how you may want to do this).
- In that URL, pass token as query-string which the client can use.
- Client will call back to the `/users/reset_password/confirm/` endpoint with the user's token, email, and new password to reset the password.
