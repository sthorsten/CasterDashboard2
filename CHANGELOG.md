# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

-


## [2.6.0-alpha] - 2022-05-04

### Notes

- Most basic features are already implemented. You **can** use this in a production environment,
but be aware that there are a lot of features still missing or unstable. **Use at your own risk!**

### Added

- Page meta information (title, description)
- Start Overlay including two variants: Logo mode (default) and full mode (including team names and colors) (#29)
- InGame Overlay (#29)
- Match details page (#28)
- Ability to remove operator bans
- Ability to remove rounds including confirm dialog
- Added confirm dialog when finishing a map
- Added automatic names for matches when not set manually (e.g. via the admin dashboard)
- News section on the home page to keep users up to date with latest releases.


## Changed

- Re-enabled Server Side Rendering (SSR)

## Fixed

- User Overlays were not being created when creating a new user
- Bug with the new start overlay not showing map score for BO1's


## [2.5.0-alpha] - 2022-04-16

### Notes

- This release is not ready for production yet!

### Added

- Season page with the ability to view, create and edit seasons
- Added charts / statistics to rounds page

### Fixed

- Season filtering not working correctly when trying to create a new playday


## [2.4.0-alpha] - 2022-04-09

### Notes

- This release is not ready for production yet!

### Added 

- Playday page with the ability to view, create and edit playdays

### Fixed

- Backend main receiver method names
- Match map score not updating correctly when score is 5-5 or higher
- Added pagination to match list page
- Fixed icon margins in various places
- Fixed win type badge not showing correctly in match and match map overview pages


## [2.3.0-alpha] - 2022-04-04

### Notes

- This release is not ready for production yet!

### Added 

- Teams page with the ability to view, create and edit teams
- Placeholder files for pages without content
- Content for the home page (temporary)

### Removed

- Old source code including the old frontend and old overlay css / scss files

### Fixed

- Version info not showing correctly in the dashboard
- Version info at the bottom of the README file


## [2.2.0-alpha] - 2022-04-02

### Notes

- This release is not ready for production yet!

### Added 

- New backend overlay models
- New frontend mapban overlay based on tailwindcss
- Updated various dependencies

### Fixed

- New user creation failed in post_save hook because the profile couldn't be created (see #23)
- Removed outdated install instruction notice from README 


## [2.1.0-alpha] - 2022-03-25

### Notes

- This release is not ready for production yet!
- Versioning will now continue according to Semantic versioning (2.1.0-alpha > 2.2.0-alpha, etc.)

### Breaking / Added

- First release of the completely reworked version
- This release includes basic match functionality
  - Create new matches
  - Map Ban
  - Map Overview
  - Operator Bans
  - Rounds
- Most data (except overlays) can be managed via the Django admin dashboard


## [2.0.0-alpha5] - 2021-02-18

### Notes

- This release is not ready for production yet!

### Added

#### Dashboard pages

- Operator Bans
- Rounds
- Overlay Control Center
- Overlay Customization
  
#### Overlays
- Start Overlay
- Maps Overlay
- InGame Overlay
  
#### Other additions
- Added Docker images to the Github Container Registry
- Added automated docker builds via Github actions 
- Added overlay customization (InGame Overlay only, WIP)
- Added some more websockets

### Changed

- The program now consists of 3 docker images: `frontend`, `backend` and `nginx`

### Fixed
- Various docker-related things
- Websocket backend connections (e.g. Django ASGI)
- nginx reverse proxy config

### Removed

- Old Docker Hub images


## [2.0.0-alpha4] - 2021-01-27

### Notes

- This release is not ready for production!

### Added

- New Nuxt Frontend (WIP)
- Notifications for all users on the home page, controllable via the Django admin panel
- Environment files for Django and Nuxt for easier configuration

### Changed

- Internal Docker workings: Added new Nuxt frontend in static mode
- Internal Docker settings to work with the new environment files

### Deprecated

- Various parts in the Django backend - will be removed step by step
- "Old" Vue frontend (being converted to Nuxt, WIP)

### Removed

- Some static files left in the Django project
- Django Landing page app (Will be handled by the new frontend and never got implemented)



## [2.0.0-alpha3] - 2020-12-22

### Notes
- This release is not ready for production!

### Added
- New Frontend Framework: VueJS
- The dashboard is now available as a Docker image
- Various Django Rest Framwork API endpoints to go along with the new frontend
- Various Websocket endpoints to get realtime updates in the new frontend

### Changed
- Complete refactoring of various components of the project
- Added more information and screenshots to the [README](README.md)

### Deprecated
- Django Views, with the exception of Django Rest Framework under /api, will be removed soon

### Removed
- Old Django Migrations

### Security
- Changed password hashing algorithm to argon2id



## [2.0.0-alpha2] - 2020-08-26

### Added
- VERSION file to display the current version in the footer
- Overlay customization page for Start and InGame Overlays (WIP)
- Profile auto-creation test

### Changed
- The Map Pick & Ban page now loads and sends data via async jQuery calls
- The Team creation process now loads and sends data via async jQuery calls
- Moved Map / Operator / Win Icons from the media to the static directory
- Added features and updated version badge in the [README](README.md) file

### Fixed
- Duplicate league entries showing on the league, season and sponsors page (Closed #1)
- Minor bugs (see commits [6ef992e](https://github.com/sthorsten/CasterDashboard2/commit/6ef992e7e14ae5177b34dc1a2261811b042697d3), [e59c854](https://github.com/sthorsten/CasterDashboard2/commit/e59c8549160e30947fc7465b9e1701d78b2a4848) and [ddaa3c8](https://github.com/sthorsten/CasterDashboard2/commit/ddaa3c87a5961efa5697f6e6fe768d2b12abfab1))



## [2.0.0-alpha1] - 2020-08-17
- First Alpha Release

### Added
- (New) Repository initialized
- Readme, Changelog and License added and updated


[Unreleased]: https://github.com/sthorsten/CasterDashboard2/compare/v2.6.0-alpha...HEAD
[2.6.0-alpha]: https://github.com/sthorsten/CasterDashboard2/releases/tag/v2.6.0-alpha
[2.5.0-alpha]: https://github.com/sthorsten/CasterDashboard2/releases/tag/v2.5.0-alpha
[2.4.0-alpha]: https://github.com/sthorsten/CasterDashboard2/releases/tag/v2.4.0-alpha
[2.3.0-alpha]: https://github.com/sthorsten/CasterDashboard2/releases/tag/v2.3.0-alpha
[2.2.0-alpha]: https://github.com/sthorsten/CasterDashboard2/releases/tag/v2.2.0-alpha
[2.1.0-alpha]: https://github.com/sthorsten/CasterDashboard2/releases/tag/v2.1.0-alpha
[2.0.0-alpha5]: https://github.com/sthorsten/CasterDashboard2/releases/tag/v2.0.0-alpha5
[2.0.0-alpha4]: https://github.com/sthorsten/CasterDashboard2/releases/tag/v2.0.0-alpha4
[2.0.0-alpha3]: https://github.com/sthorsten/CasterDashboard2/releases/tag/v2.0.0-alpha3
[2.0.0-alpha2]: https://github.com/sthorsten/CasterDashboard2/releases/tag/v2.0.0-alpha2
[2.0.0-alpha1]: https://github.com/sthorsten/CasterDashboard2/releases/tag/v2.0.0-alpha1

