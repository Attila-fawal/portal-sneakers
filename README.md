
# Portal-Sneakers 


Welcome to the Portal Sneakers, the ultimate online destination for sneaker enthusiasts around the globe. Whether you're on the hunt for the latest drops, classic retros, or seeking feedback from our passionate community, this platform has got you covered.

![Screenshot (77)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/b641ca81-809e-4ea3-948f-229e9d499e1f)

## Overview
Portal Sneakers offers a modern e-commerce experience dedicated to sneakerheads. With a variety of features tailored to provide a seamless browsing and shopping experience, users can explore a vast inventory, manage their orders, and interact with the community.
![Screenshot (78)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/badcb2d0-41aa-481e-9706-4f4550b3d9b3)

## As a Site Owner, you can:

- Manage product listings and inventory.
- Monitor user activities and order histories.
- Engage with the community via reviews and feedback.
- And get user information for future marketing.

![Screenshot (79)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/f6a25263-1f78-4c00-b3f0-fae7623e095a)

## As a Customer, you can:

- Browse a vast collection of sneakers with detailed information.
- Shop securely with a user-friendly cart and checkout system.
- Keep track of desired items with a personalized wishlist.
- Engage with the sneakerhead community, reading and leaving reviews.

![Screenshot (80)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/a6095148-3ee6-443b-998e-f0a0f5d9e881)


## Features
- User Authentication: Secure login and registration functionalities ensure user data protection and personalized experiences.
- Product Listings: A comprehensive inventory of sneakers with detailed specs, pictures, and dynamic filters.
- Shopping Cart: Easily add sneakers to the cart and enjoy a hassle-free checkout experience.
- Order History: Review past purchases and track current orders in real-time.
- Ratings & Reviews: Share feedback and read reviews from other sneakerheads.
- Wishlist: Save sneakers for later or manage a dynamic list of desired products.
- Messaging & Notifications: Integrated Django messaging system keeps users informed about orders, updates, and more.

![Screenshot (81)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/60d078e2-3d4a-4d61-9dbe-74ff9298e5a7)


## Brief Description for the current apps in the project

### Profile App Description
![Screenshot (83)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/2ec40456-6398-4bb3-b4eb-b46aefc085fc)

The Profile App serves as the hub for users to manage their personal information and preferences on the platform. It is integral for creating a personalized user experience. Here are the primary features:

- User Profile Management:

It presents a detailed user profile, allowing members to view and update their personal and delivery information. Fields like phone number, address, city, county, postal code, and country are maintained.
New profiles are automatically created upon user registration and are updated as necessary.

- Wishlist Functionality:

Users can create a wishlist, a curated list of products they desire.
The app provides functionalities to add and remove products from this wishlist, making it dynamic based on user preferences.

- Order History:

A consolidated view of all past orders, allowing users to revisit and check the specifics of their purchases. For every order, a confirmation message is displayed, reiterating details shared during the purchase.

- Feedback System:

The built-in messaging mechanism gives real-time feedback on various user actions. Whether they've successfully updated their profile, added items to their wishlist, or encountered errors, instant messages guide them through the process.
The Profile App harnesses Django's powerful ORM features, including signals to automate the creation and update of user profiles and wishlists post user registration. This ensures data consistency and improves user experience. It also integrates with the Product and Checkout apps, indicating a comprehensive e-commerce solution.

### Product App Description
![Screenshot (87)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/afc6e4b6-c565-4549-9122-0e59b13d4067)
![Screenshot (88)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/bf22ae27-742d-45d4-be08-8c3568cb5e47)


- Models:

Category:
Represents a type or category under which products can be classified.

Fields:
name: A string that denotes the name of the category.

friendly_name: A user-friendly display name for the category which can be optionally set.

Methods:
get_friendly_name(): Returns the friendly name of the category.

Product:
Represents individual products being sold.

Fields:
category: Foreign key relation to the Category model, representing which category a product belongs to.

sku: Stock Keeping Unit, a unique identifier for products.
name: Name of the product.

description: Text description detailing the product.

price: Decimal representation of the product's price.

rating: An optional field for the product's rating.

image_url: An optional URL where the product's image can be found.

image: An image field that stores the product's image.

Size:
Represents available sizes for products.

Fields:
size: Integer field denoting the size value.

size_type: Choice field specifying the type of size (Men, Women, Kids).

ProductSize:
Represents the relationship between products and their available sizes.

Fields:
product: Foreign key relation to the Product model.

size: Foreign key relation to the Size model.

quantity: Number of products available in that particular size.

- Views:

all_products:
Lists all products. Supports sorting, searching, and category filtering functionalities.

product_detail:
Displays details for an individual product. Integrates a comment system for users to leave feedback.

add_product:
Allows store owners (superusers) to add a new product. Uses formsets for managing product sizes.

get_sizes:
A view to fetch sizes based on category. Returns sizes in JSON format for dynamic frontend functionalities.

edit_product:
Allows store owners to edit the details of a product. Uses inline formsets to handle associated product sizes.

delete_product:
Provides store owners with functionality to delete a product.

- Forms:

Utilizes Django's form system for creating and editing products. This includes the main product form (ProductForm) and an inline formset (create_product_size_formset) for handling multiple sizes associated with a product.

- Decorators:

Uses the @login_required decorator to ensure certain views are accessible only by logged-in users.

Additional checks within views ensure only superusers (store owners) can add, edit, or delete products.

- Flow:

Store owners can add, edit, or delete products, each product having one or more sizes.
Customers can view products either in a list format or detailed view.
Products can be sorted, searched, or filtered by category.
Detailed view integrates a comment system for user reviews and feedback.

### Comments App Description

![Screenshot (82)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/4d542062-ef57-4192-ad5c-8b4e0236da83)
- Models:

Comment:
Represents user comments associated with products.

Fields:
user: A foreign key to Django's default User model. Represents which user made the comment.

product: A foreign key to the Product model, indicating which product the comment is about.

text: A text field containing the main content of the comment.

rating: An integer field allowing users to rate a product (from 1 to 5).
created_date: Date and time when the comment was created.

modified_date: Date and time when the comment was last modified.

String Representation:
Returns a truncated version of the comment followed by the user's username and the product name.

- add_comment:
Allows logged-in users to add a comment to a specific product.

If the form submission is valid, it associates the comment with the user and the product, then saves it.

After saving, it redirects the user back to the product detail page.

- edit_comment:
Allows logged-in users to edit their own comments, provided they are the author or they have superuser privileges.

If a user tries to edit a comment they didn't author and they aren't a superuser, the template will not render edit and delete button.

After successful editing, users are redirected back to the product detail page.

- delete_comment:
Allows logged-in users to delete a comment.

A user can delete a comment if they are the author or have superuser privileges.

After deletion, the user is redirected back to the product detail page.

- CommentForm:
A form for adding or editing comments.
Contains fields to enter the comment text and optionally rate the product.
Decorators:
Uses the @login_required decorator for all views to ensure only logged-in users can add, edit, or delete comments.

- Flow:

Users can view a product's details and choose to leave a comment.
They can rate a product and leave text feedback.
Users can only edit or delete their own comments unless they are superusers.
All interactions with comments result in feedback messages for the user (e.g., "Successfully added comment!")

### Checkout App Description
![Screenshot (85)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/71cc8440-9b7d-43da-a0cb-923afe5aa639)


The Checkout app in the e-commerce platform orchestrates the process of finalizing a user's purchase and capturing their payment.

- Key Functionalities:

Payment Integration: The app integrates with Stripe, a renowned payment gateway, ensuring secure and seamless financial transactions. Through the provided views, there's a clear flow from initializing a payment intent to processing the payment.

- Order Management:

Upon a successful checkout, an order is created with all the requisite details, such as the user's contact information, delivery address, and the products they've bought.

Each order generates a unique order number using the UUID system, ensuring every transaction is distinctly identifiable.

- Order Line Items:

For granularity, every product within an order is listed as an individual "Order Line Item." This approach provides a detailed breakdown, capturing specific product details like its size, quantity, and the total price for that item.

- User Experience Enhancements:

If users have previously filled their details and have a profile, the app pre-populates the checkout form with their saved data. This intuitive feature reduces the steps needed to complete a purchase.

Feedback mechanisms are integrated throughout; users are promptly informed about issues like an empty cart or missing product data.

- User Profiles:

Post-purchase, the app offers an option to save the user's shipping information to their profile, making future checkouts even more streamlined.

- Robust Error Handling:

Throughout the checkout process, users are kept informed. If any hiccup occurs – be it a missing product in the database or a payment issue – users are immediately alerted with descriptive error messages.

- Models:

Order: Represents the core of the app. This model captures comprehensive details about each purchase, from the user's contact information to the aggregate cost.

OrderLineItem: This auxiliary model provides a detailed breakdown of each product within an order, from its size and quantity to its subtotal.

### Bag App Description
![Screenshot (84)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/bec7e404-7ad2-4d8d-9bfb-eeec8ae347e7)

![Screenshot (89)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/c67e0567-0b27-4bfb-b769-ed96ef7d2027)


#### Features & Functionalities:

- View Bag:

Function: view_bag
Users can view the contents of their shopping bag, providing a summary of the items they've selected to purchase.

- Add to Bag:

Function: add_to_bag
Products can be added to the shopping bag based on product ID.

Users can specify the desired size and quantity of the product.

The system checks if the requested quantity is available in the inventory and validates the quantity input.

Feedback messages inform users of successful additions or potential issues, like inventory shortages.

Utilizes the ProductSize model to manage inventory by product size.

- Adjust Bag:

Function: adjust_bag
Allows users to modify the quantity of a particular product in their shopping bag, based on size.

Performs validations like ensuring the quantity doesn't exceed available inventory and that the quantity is at least 1.

Provides feedback through messages on successful adjustments and potential issues.

Utilizes JSON responses to facilitate a more dynamic front-end interaction, returning the success status and redirect URLs.

- Remove from Bag:

Function: remove_from_bag
Facilitates the removal of products from the shopping bag, based on the product's ID and size.

Ensures that the product and its specified size exist in the bag before attempting removal.

Provides feedback messages for successful removals and potential issues.
As with the adjust_bag function, it uses JSON responses for front-end interactions.

- Integrated Models:

The Bag App interacts heavily with the Product and ProductSize models from the products app. This integration ensures that the bag accurately reflects the available products and inventory.

- Error Handling:

Each function contains robust error handling mechanisms. Users are informed of any issues during their interactions, such as trying to add more products than available in the inventory or attempting to remove a non-existent item.
Utilizes Django's messages framework for feedback and error reporting to users.

- Session Management:

The Bag App relies on Django's session management to keep track of a user's shopping bag across their browsing experience. This ensures that users don't lose their selected items even if they navigate away from the bag page.

## Bugs
- The Quantity field in the Bag template not rendering the changed quantity on large screen. But the function is working And On small screen everything working fine.
## Validator and testing
- PEP8 style guide and validated HTML and CSS code.
![Screenshot (99)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/683863dd-8da5-48b6-a978-762856497639)

![Screenshot (100)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/a430151e-c4a8-4f6b-8522-cdea80c690e0)

![Screenshot (101)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/5862825e-b156-4cc4-b053-7a7838a004e3)

![Screenshot (102)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/089d26ef-7bba-46a5-b767-8ed42291d0b6)

- Device & Browser Testing: Ensure cross-browser and cross-device compatibility. Test on various devices (mobile, tablet, desktop) and browsers (Chrome, Firefox, Safari, Edge).

- Responsive Design: Ensure the UI is responsive. Elements should adjust and look good on different screen sizes.

- Error Messages: Verify that appropriate and user-friendly error messages appear when required.

- Loading Time: Check the speed of the web application. It should load quickly and not keep users waiting.

- Links: Ensure all internal and external links are working as expected.

- Profile App:
User Profile Creation:

Verify that a new profile is created automatically upon user registration.
Check if all fields (phone number, address, etc.) can be edited and saved correctly.
Wishlist:

Add items to the wishlist and ensure they appear correctly.
Remove items from the wishlist and verify they are removed.
Order History:

After purchasing, ensure the order appears in the history.
Test the view and interaction for multiple orders.
Feedback System:

Check if messages appear correctly for various user actions.
- Product App:
Product Listing:

Ensure all products appear with accurate images, descriptions, and categories.
Test filtering, searching, and sorting functionalities.
Product Detail:

Each product's details should be accurate and well-displayed.
Comments and ratings for the product should load correctly.
Superuser Capabilities:

Verify that only superusers can add, edit, or delete products.
Test the addition, editing, and deletion processes.
- Comments App:
Add Comment:

Ensure users can add comments to products.
Check if ratings and feedback save and appear correctly.
Edit Comment:

Users should be able to edit their comments.
Ensure unauthorized users cannot edit others' comments.
Delete Comment:

Ensure users can delete their comments.
Unauthorized users should not be able to delete others' comments.
- Checkout App:
Payment Process:

Go through the payment process. Use sandbox testing environments for payment gateways to avoid real transactions.
Test with different payment methods if available.
Order Creation:

After payment, ensure the order is saved with all correct details.
Order Line Items:

Items within an order should have accurate details, including size, quantity, and price.
Error Handling:

Test edge cases and unexpected scenarios, like unplanned exits during payment.
- Bag App:
Add to Bag:

Add products to the bag and verify they appear correctly.
Try adding products beyond inventory limits and verify the appropriate response.
Adjust Bag:

Change product quantities and verify they update correctly.
Ensure correct responses for edge cases, like setting quantity to zero.
Remove from Bag:

Remove products and ensure they are no longer in the bag.
Session Management:

Products in the bag should persist even if the user navigates away or closes the browser.
- Usability & Accessibility:
Ease of Use: Ensure the website is user-friendly, with intuitive navigation and design.

Accessibility: Check for good color contrast, font readability, and keyboard navigation. Consider tools like WAVE or AXE for accessibility testing.

- Security:
Authentication & Authorization:

Verify login and registration processes.
Ensure that user data is encrypted and passwords hashed.
Unauthorized users should not be able to access privileged actions or views.
Input Validation:

Test forms with invalid or malicious data to ensure strong validation.

## Deployment
- This project was deployed Using Code-Institute-Org/ci-full-template.

- The project was deployed to GitHub Pages using the following steps...

In the GitHub repository, navigate to the Settings tab
From the source section drop-down menu, select the Main Branch
Once the main branch has been selected, the page will be automatically refreshed with a detailed ribbon display to indicate the successful deployment.

-  1 Local Deployment:

Dependencies: Install all required packages from your requirements.txt Ensure all required dependencies are downlodad. pip install -r requirements.txt


Environment Variables: make sure you have a local .env file or other mechanisms to load them in your local environment.

Run the App Locally:

Start the Django development server:
python manage.py runserver


- 2 deployment to heroku:

Fork or clone this repository.

create new heroku account or if you already have one press to create a new app.

Add name for your new app And choose the region Go to settings and add buildpacks python.

- Set the necessary environment variables:
- AWS_ACCESS_KEY_ID,
- AWS_SECRET_ACCESS_KEY,
- USE_AWS,
- DATABASE_URL,
- EMAIL_HOST_PASS, 
- EMAIL_HOST_USER, 
- SECRET_KEY, 
- STRIPE_PUBLIC_KEY, 
- STRIPE_SECRET_KEY, 
- STRIPE_WH_SECRET.

If not already done, create a Procfile :

web: gunicorn portal_sneakers.wsgi:application.

Link the Heroku app to the repository
Click the Deploy

DEBUG should be False in production.
Always backup your data before migrating.

and robots.txt, sitemap.xml

## Credits
code Institute For the deployment terminal.

Boutique Ado for the basis

ElephantSQL for the database.

aws for storage to Pictures.

fontawesome for the icons.

stripe for Payment processor.

mailchimp for pop up email.

## Portal-Sneakers E-Commerce Application Keyword Analysis
### Short-Tail Keywords:
- Sneakers for sale
- Women's sneakers
- Men's sneakers
- Kids' sneakers
- Affordable sneakers
- Trendy sneakers
- Athletic shoes
- Running shoes
### Long-Tail Keywords:
- Online sneakers store
- Buy sneakers online
- Best sneakers deals
- Designer sneakers for women
- High-quality men's sneakers
- Comfortable kids' sneakers
- Fashionable sneakers for all ages
- Top-rated sneakers store
- Popular sneaker brands
- Casual sneakers collection
- Sneaker discounts and offers
- Latest sneaker releases

## portal Sneakers : Product Page
- What do your users need?

Clear images of the sneaker from various angles
Product details (size, color variations, material, etc.)
Price and availability status
User reviews and ratings
Care instructions for the sneaker
A way to purchase or add the product to the cart

- What information and features can you provide to meet those needs?

A zoomable image gallery of the sneaker.
Product description section with size chart link.
Real-time stock availability.
User reviews section with a filter option.
Add to cart or buy now button.
Secure payment gateway integration.

- How can you make the information easy to understand?

Use bullet points for quick product specs.
Offer a Q&A section for user-submitted questions and answers.
Use simple and straightforward language in the description.
Use icons to signify features like "Free Shipping", "100% Authentic", etc.

- How can you demonstrate expertise, authoritativeness, and trustworthiness in your content?

Provide links to official brand pages.
Offer "Certified Authentic" badges or similar trust signals.
Allow verified purchase users to leave reviews.
Provide detailed care instructions and possibly a blog post on sneaker maintenance.

- Would there be other pages within your own site you could link to from your chosen page?

Related products or "You might also like" section.
Blog posts about sneaker trends, care, or the history of the sneaker model.
Brand's main page on your platform.
Link to a return and refund policy page.

- Are there opportunities to link back to external websites that already rank highly on Google?

Link to the official Nike page for the product or to any press release related to that sneaker model.
Link to sneaker review websites or blogs that discuss the product.

- How can you help users discover other relevant parts of your web application?

Breadcrumbs at the top for easy navigation (e.g., Home > Nike > Air Force 1).
Promote seasonal sales or featured collections.
Sidebar or footer links to top categories or brands.

## portal Sneakers E-commerce Store: Marketing Plan

- Who are your users?

Sneaker enthusiasts and collectors.
Individuals looking for trendy or performance footwear.
Gift shoppers.
Athletes and fitness enthusiasts.

- Which online platforms would you find lots of your users?

facebook, Instagram, given its visual nature and popularity among fashion-forward users.
Sneaker forums and communities.
YouTube, where sneaker reviews and unboxings are prevalent.

- Would your users use social media? If yes, which platforms do you think you would find them on?

Yes, they would use social media.
Instagram: Due to its visual appeal and the prevalence of sneaker influencers.
Twitter: For latest sneaker drops, news, and discussions.
Facebook: Community groups dedicated to sneaker collections and trades.
TikTok: Short video content on sneaker reviews, fashion, and unboxing.

- What do your users need? Could you meet that need with useful content? If yes, how could you best deliver that content to them?

Users need detailed reviews, information on upcoming releases, sneaker care tips, and styling ideas.
Blog Posts: Detailed guides and articles.
YouTube Channel: Video reviews and unboxings.
Instagram Stories: Sneak peeks of upcoming releases.

- Would your business run sales or offer discounts? How do you think your users would most like to hear about these offers?

Yes, especially during festive seasons, clearance sales, or to promote a new collection.
Email Marketing: Send out newsletters with exclusive offers.
Social Media: Promotional posts and stories.
Push Notifications: Instant updates for mobile app users.

- What are the goals of your business? Which marketing strategies would offer the best ways to meet those goals?

Goals: Increase brand recognition, boost sales, create a loyal customer base.
Influencer Collaborations: Partner with sneaker influencers for broader reach.
Affiliate Marketing: Collaborate with sneaker blogs and YouTubers.
Content Marketing: Regular blog posts and YouTube videos for SEO and user engagement.
Paid Advertising: Targeted ads on social media platforms like Instagram and Facebook.

- Would your business have a budget to spend on advertising? Or would it need to work with free or low cost options to market itself?

Starting off, budget might be limited, so emphasis on organic growth through content marketing, community engagement, and collaborations.
As revenue grows, consider allocating a budget for paid advertising and expanded influencer partnerships.


## facebook page 
link: https://www.facebook.com/profile.php?id=100095685485170

![Screenshot (90)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/a0c0357d-d532-4a7c-b1b6-6879de188b13)



and the project link: https://portal-sneakers-b3943e09f616.herokuapp.com



## Wireframes

![Screenshot (103)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/0f029323-8dc7-4425-b536-e45e36ee479a)
![Screenshot (104)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/ce7e05dd-794b-4dad-80ad-590dcabc82b7)
![Screenshot (109)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/60906aca-9be1-42b9-9081-972faddf9307)
![Screenshot (113)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/fb729986-e629-4821-bc46-00c401306d2c)
![Screenshot (111)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/50260577-902a-44f1-99b3-cb6d6ebd976c)
![Screenshot (112)](https://github.com/Attila-fawal/portal-sneakers/assets/127791713/d6c83722-28ce-4ec3-8b37-ef888d8209da)





















