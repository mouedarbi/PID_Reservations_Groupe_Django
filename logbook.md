Logbook
Date: Wed Jan 21 2026
Progress Summary
This session focused on analyzing the project's current state, setting up a development branch, implementing a new API endpoint, addressing an authentication issue by creating a superuser, and writing and fixing tests for the new API.

1. Project State Analysis
Git Status: The project is on the dev_ghiles branch, which is up-to-date with origin/dev_ghiles. The working tree is clean.
Recent Commits: Reviewed the last 5 commits, noting merges and CI pipeline fixes, indicating active development.
Project Description: Confirmed it's a Django-based reservation system for shows, featuring a catalogue, online reservations, admin back-office, RESTful API, and a planned ReactJS frontend (from README.md).
Dependencies: Identified key dependencies from requirements.txt and README.md, including Python 3.11+, Django 5.0.14, Django REST Framework, MySQL/MariaDB 11+, and Bootstrap 5.
Database Migrations: Verified that all migrations for admin, auth, authtoken, catalogue, contenttypes, and sessions apps are applied. The api app currently has no migrations.
Virtual Environment: Initially, python manage.py commands failed due to the virtual environment not being activated or dependencies not installed within the shell context. This was resolved by using the full path to the python executable within the venv folder.
2. Branch Creation
Created and switched to a new Git branch named TESTING as requested by the user, for testing purposes.
3. Localities API Implementation
Model Inspection: Reviewed the Locality model in catalogue/models/locality.py, noting its postal_code and locality fields.
Serializer Update: Modified api/serializers/localities.py.
Changed from serializers.Serializer to serializers.ModelSerializer.
Corrected field exposure to id, postal_code, and locality, aligning with the Locality model.
Removed zip_code as it did not exist in the Locality model and was an inconsistent field name in the previous placeholder serializer.
Views Implementation: Updated api/views/localities.py.
Replaced placeholder APIView implementations with Django REST Framework's generic views: generics.ListAPIView for fetching a list of all localities and generics.RetrieveAPIView for fetching a single locality by its ID.
Explained that this change simplifies the code and aligns with DRF best practices, as generic views encapsulate common API logic.
Routes: Confirmed that the routes in api/urls.py for /localities/ and /localities/<int:id>/ were already correctly configured and pointed to the respective views, requiring no further modifications.
4. Authentication Issue and Superuser Creation
Error Diagnosis: Addressed an HTTP 403 Forbidden error ("Authentication credentials were not provided"), explaining that the API endpoint requires authentication.
Superuser Creation: Created a Django superuser named admin with the email admin@gmail.com via the createsuperuser management command. Password validation was bypassed during creation. This superuser can now be used for API authentication.
5. API Testing and Fixing
Test Creation: Created a new test file api/tests/test_localities.py, using api/tests/test_prices.py as a template. The new tests cover listing and retrieving localities for both authenticated and unauthenticated users, as well as handling non-existent localities.
Initial Test Failure: The initial test run failed with an AssertionError. The error indicated that the LocalitiesDetailView expected a URL keyword argument named pk, but the URL was configured with id.
Git Commit: As requested, the new test file was committed with the message "AssertionError, use pk instead of id" before the fix was applied.
The Fix: The issue was resolved by adding lookup_field = 'id' to the LocalitiesDetailView in api/views/localities.py. This change aligns the view with the project's URL convention of using id as the lookup key.
Successful Test Run: After applying the fix, the tests in api.tests.test_localities were run again and all passed successfully.
Date: Mon Jan 26 2026
Progress Summary
This session focused on implementing a complete authentication API, including user signup, login, and logout. This involved creating new serializers, views, and a comprehensive test suite. A summary of the user's recent commits was also added to this logbook.

1. User Commits Summary
A summary of the user's last four commits was added to the logbook:

78368558c6ce615395bba300862e3dd8a441542c: API test locations v.0
aaed9597e3ac9470396930d819e92cf30eff092e: feat(api): Implement staff-only CRUD for Locations and Localities & Update test_localities.py
9d5abe05892d9c19868320faa466466dd8c0cd03: API locations & localities modified v2
47dafe721c6b019c812e70d457c32408b197b942: API locations & localities modified
2. Authentication API Implementation
Analysis: Analyzed the project to determine the correct approach for implementing token-based authentication using Django REST Framework's built-in TokenAuthentication.
Serializers:
Created api/serializers/signup.py with a SignUpSerializer for user registration. The serializer handles username, password, email, first_name, last_name, and langue. It also adds new users to the MEMBER group and creates a UserMeta object.
Updated api/serializers/auth.py to use DRF's AuthTokenSerializer for the login view.
Views:
Implemented AuthSignupView, AuthLoginView, and AuthLogoutView in api/views/auth.py.
AuthSignupView (generics.CreateAPIView) uses the SignUpSerializer to create new users and returns an auth token upon successful registration.
AuthLoginView (subclass of ObtainAuthToken) handles user login and returns a token.
AuthLogoutView (APIView) deletes the user's token to log them out.
Testing:
Created api/tests/test_auth.py with a comprehensive test suite.
Tests cover successful and unsuccessful signup (e.g., missing fields, existing username), login (correct and incorrect credentials), and logout (authenticated and unauthenticated users).
Debugged and fixed initial test failures, including a 403 vs. 401 status code issue for unauthenticated logout and ensuring required fields in the signup serializer were enforced.
File Management: Accidentally deleted and then restored the api/serializers/signup.py file, confirming the fix by re-running the test suite.
Date: Mon Jan 26 2026
Progress Summary
This session focused on fixing failing API tests for localities and locations to ensure a successful merge with the pre-production environment. The main problem was that unauthenticated access to these APIs was returning 403 Forbidden instead of the expected 200 OK for existing resources or 404 Not Found for non-existent ones.

1. Fixes for Localities and Locations API Permissions
Problem Diagnosis: Identified that several tests in test_localities.py and test_locations.py were failing due to 403 Forbidden responses for unauthenticated GET requests, and 400 Bad Request errors during location creation/update.
Permissions Refactoring:
Implemented the get_permissions method in api/views/localities.py (LocalitiesView, LocalitiesDetailView) and api/views/locations.py (LocationsView, LocationsDetailView).
This method now dynamically assigns permissions: [AllowAny()] for GET requests (allowing public read access) and [IsAdminUser()] for POST, PUT, PATCH, and DELETE requests (restricting write operations to admin users).
Removed redundant manual request.user.is_staff checks within the view methods, promoting declarative permission handling.
Serializer Validation Fix:
Addressed 400 Bad Request errors during location creation and update by explicitly defining the website field in api/serializers/locations.py (LocationSerializer).
The website field was set with required=False, allow_null=True, and default=None to correctly handle its optional nature as defined in the Location model.
Verification: All tests for api.tests.test_localities and api.tests.test_locations now pass successfully, confirming the resolution of the permission and validation issues.
Date: Mon Jan 26 2026
Progress Summary
This session focused on fixing a critical IndentationError in api/views/shows.py that was breaking the application.

Error Diagnosis: An IndentationError was identified in api/views/shows.py, caused by an incorrectly indented docstring. A subsequent fix attempt then introduced a SyntaxError due to a misplaced class docstring that improperly wrapped a method definition.
Code Refactoring:
Corrected the indentation of all docstrings within the file.
Restructured the class definitions for ShowsView and ShowsDetailView to properly separate the class docstring from method definitions.
Added missing imports for permissions and status from rest_framework to resolve NameError issues.
Verification: After refactoring, the application's test suite was run. It passed without any syntax or indentation errors, confirming that the file is now correctly formatted and loadable by Django.
Version Control: The corrected file was committed to the feature/frontend-mvp branch and pushed to the remote repository.
Date: Mon Jan 26 2026
Progress Summary
This session involved comparing the dev_noureddine branch with the pre-production branch and then merging dev_noureddine into feature/frontend-mvp.

1. Branch Comparison
dev_noureddine vs. pre-production:
Commits unique to dev_noureddine:
aa34ad7: Implementation of the ticket, checkout, and rss API endpoints.
546bede: Implementation of the artist-types API (linking Artist and Type).
34249cc: Correction of the reservation API, including security and tests.
Commits unique to pre-production: (representing work from other developers and merged features)
Significant frontend implementation (Django frontend app, templates, static files, views).
API fixes and features: Syntax correction in api/views/shows.py, re-authentication for Show views, PricesAPI test updates, requirements.txt correction, admin permissions for price creation in PricesView, and .idea/ file ignoring.
CI/CD improvements (runner and MySQL service for tests).
Other API implementations for Price and Localities.
2. Merge dev_noureddine into feature/frontend-mvp
Merge Execution: The dev_noureddine branch was merged into the current feature/frontend-mvp branch.
Conflicts: As anticipated, conflicts arose in api/test/test_reservation.py (modify/delete) and api/urls.py (content).
Conflict Resolution: The user indicated that they would manage the conflicts in PyCharm. After manual resolution, git status confirmed that all conflicts were resolved and staged.
Version Control: The merge commit was created and pushed to the remote feature/frontend-mvp branch, integrating the changes from dev_noureddine.

**Date:** Mardi 27 janvier 2026

**Branch:** `dev_ghiles`

**Summary of Actions:**

1.  **Project Setup and Context**: Initial project directory and structure were understood.
2.  **Git Workflow & Branch Management**:
    *   Created a `TESTING` branch for development.
    *   Integrated work from `TESTING` into `dev_ghiles` via merge.
    *   Committed changes on `TESTING` and `dev_ghiles` with relevant messages (e.g., "Feat: Implement location detail page, About Us page...", "Frontend locations & about us", "Fixing frontend locations & about us pages").
    *   Pushed `dev_ghiles` to the remote repository.
    *   Deleted the local `TESTING` branch.
    *   Reset `dev_ghiles` locally to match `origin/dev_ghiles` to ensure synchronization and discard any divergent local changes.
3.  **Database Migrations & Fixtures**:
    *   Managed database migrations for the `catalogue` app, including faking one migration (`catalogue.0023`) due to constraint issues.
    *   Successfully loaded several fixture files (`artist_type.json`, `prices.json`, `shows.json`, `representations.json`, `reviews.json`, `types.json`, `auth_user.json`, `user_meta.json`).
    *   Skipped loading `artists.json`, `localities.json`, `locations.json` as data was already present.
    *   Skipped `reservations.json` due to a structural issue in the fixture file.
4.  **Feature Implementation: Location Detail Page**:
    *   Created a new URL pattern (`/locations/<slug>/`), view (`location_detail`), and template (`location_detail.html`).
    *   Updated `location_list.html` to make location cards clickable links to their detail pages, displaying only names.
    *   Ensured all 7 locations are displayed on the list page.
5.  **Feature Implementation: About Us Page**:
    *   Added a URL pattern for `/a-propos/`.
    *   Defined an `about_us` view in `frontend/views.py`.
    *   Created an `about.html` template.
    *   Updated the navigation link in `base.html` to point to the new about page.
6.  **UI/Layout Fixes**:
    *   **Title Overlap**: Added `padding-top: 80px;` to the `main` tag in `base.html` to ensure page titles are not hidden behind the fixed navigation bar.
    *   **Login/Logout Links**: Styled "Connexion" and "Déconnexion" as text navigation links (`nav-link` class) with white text, preserving functionality. Restored JS logout mechanism and hidden form.
7.  **Cart Models**:
    *   Created `Cart` and `CartItem` models in `catalogue/models/cart.py`.
    *   Updated `catalogue/models/__init__.py` to include cart models.

---

**Date:** Mardi 27 janvier 2026
**Branch:** `dev_ghiles`
**Developer:** `dev_ghiles`

**Progress Summary:**

This session focused on implementing a full-featured cart API, from models to views and URLs.

1.  **Cart API Implementation**:
    *   **Models**: Created `Cart` and `CartItem` models in `catalogue/models/cart.py`, establishing a one-to-one relationship between `User` and `Cart`, and linking `CartItem` to `catalogue.Representation` to track specific show instances.
    *   **Migrations**: Created and applied database migrations for the new cart models.
    *   **Serializers**: Implemented `CartSerializer` and `CartItemSerializer` in `api/serializers/cart.py` to handle data serialization, including nested items and calculated total fields.
    *   **Views**: Developed a complete set of API views in `api/views/cart.py` for cart management:
        *   `CartView`: Retrieve or create a cart for the authenticated user.
        *   `CartItemAddUpdateView`: Add new items or update quantities of existing items, including inventory checks against `representation.available_seats`.
        *   `CartItemDetailView`: Retrieve, update, or delete specific cart items, with ownership checks.
        *   `CartClearView`: Clear all items from the cart.
    *   **URLs**: Updated `api/urls.py` with endpoints for all the new cart views.

2.  **Code Review and Correction**:
    *   During the implementation of the cart views, a potential error was identified in the `get_object` method of `CartItemDetailView`.
    *   As per your astute correction, this was fixed by changing the implementation to `raise Http404`, ensuring correct HTTP error handling. Your contribution was crucial to making the code more robust.

3.  **Version Control**:
    *   The new `cart.py` model was committed with the message "New model, cart.py" and pushed to `origin/dev_ghiles`.
    *   The related serializer, view, and URL changes are staged and ready for the next commit.

---

**Date:** Mardi 27 janvier 2026
**Branch:** `dev_ghiles`
**Developer:** `dev_ghiles`

**Progress Summary:**

This session focused on completing the cart API by adding a comprehensive test suite and fixing critical bugs that were preventing the application from running.

1.  **Cart API Testing**:
    *   A complete test suite was created in `api/tests/test_cart.py` to validate the cart API's functionality.
    *   The tests cover cart retrieval, adding/updating items with inventory checks, deleting items, clearing the cart, and ownership permissions.
    *   The test's `setUp` method was refined to correctly create all necessary model instances (`Locality`, `Location`, `Show`, `Representation`) based on their actual definitions, ensuring the tests run against a valid database state.

2.  **Debugging and Critical Fixes**:
    *   **`Http404` Correction**: An error in the view code was corrected by changing `raise status.HTTP_404_NOT_FOUND` to `raise Http404`, as you pointed out.
    *   **Startup Error Fix**: Diagnosed and resolved a `SyntaxError` in `api/views/cart.py` that was preventing the website from running. The fix was verified using `python manage.py check`.

3.  **Version Control**:
    *   The complete cart API implementation (serializers, views, URLs, and tests) and the logbook update were committed with the message "Update api cart to fix bugs & creation test_cart".
