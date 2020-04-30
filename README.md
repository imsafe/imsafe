# Imsafe - Secure image storage and transfer application.

### Endpoints:

###### API Root

/api/ - [GET]

###### Authentication

api/api-auth/login/ - [POST]<br>
api/api-auth/logout/ - [GET]

###### Users 

/api/users/ - [GET] [POST]<br>
/api/users/{user_id} - [GET] [PUT] [DELETE]<br>
/api/userkeys/ - [GET] [POST]<br>
/api/userkeys/{user_id} - [GET] [PUT] [DELETE]

###### Images

/api/images/ - [GET] [POST]<br>
/api/images/{image_id} - [GET] [PUT] [DELETE]<br>
/api/images/{image_id}/decrypt/ - [POST]<br>
/api/images/{image_id}/transfer/ - [POST]
