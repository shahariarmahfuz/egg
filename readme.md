# Avatar Upload Feature

This project uses Cloudinary for user avatar uploads.

## Environment Variables

Make sure you add the following to your `.env` file:

```env
CLOUDINARY_URL=cloudinary://<your_api_key>:<your_api_secret>@diwp8ug1r
```

Replace `<your_api_key>` and `<your_api_secret>` with your actual Cloudinary API credentials.

## Requirements

The feature relies on two additional Python packages:
- `cloudinary`: To interact with the Cloudinary API.
- `Pillow`: To process (resize and compress) image uploads before sending them to Cloudinary.

These have been added to the `requirements.txt`.

## How it works

1. Users can upload an image (JPG, PNG, WEBP) from their Profile/Settings page.
2. The server uses `Pillow` to validate, compress, and resize the image to a 300x300 square.
3. The processed image is then uploaded to Cloudinary, and its URL and `public_id` are saved in the database.
4. Old avatars are deleted from Cloudinary whenever a new one is uploaded to conserve space.
5. If a user chooses to "Generate Random Avatar", any existing Cloudinary avatar is removed and a new `avatar_seed` is generated.
