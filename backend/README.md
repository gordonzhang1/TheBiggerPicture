# Backend

## Database

For now this uses Supabase (probably pretty easy to switch out for any SQL database?). There are two tables:

One is `categories` (wasn't sure what to call this) which has all the "big images"

| Name              | Type   |
| ----------------- | ----   |
| id                | number |
| name              | string |
| description       | string |
| desired_image_url | string |

`images`: stores images and their info

| Name              | Type   |
| ----------------- | ----   |
| id                | number |
| created_at        | string |
| url               | string |
| grayscale         | number |
| category          | number |

`grayscale` is a number between 0-255 indicating the "average" grayscale value of the image (allows us to arrange the images properly if we stick to grayscale). `category` is the category ID that the image is a part of

## S3

All images are stored on S3 in one bucket and UUIDs are used to ensure no duplicate image file names

## Other

there's a `requirements.txt` file to install the libraries