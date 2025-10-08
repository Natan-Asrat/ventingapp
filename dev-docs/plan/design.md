# Design

## System Architecture

- Three tier architecture
    - Client
    - Application Server
    - Data Server

![architecture](./design/system_architecture.drawio.svg)

## Subsystem Decomposition
- Component Diagram
    
    ![component diagram](./design/subsystems/decomposition.drawio.svg)

### User Subsystem

- Handles signup and login.
- Components:
    - User: Entity/Model for the User class saved on Database
    - UserViewset: Handles signup/login related requests
    - UserCreateSerializer: DTO for signup, expects all information including password
    - UserSimpleSerializer: DTO for getting user information, returns only necessary details.

![user subsystem](./design/subsystems/user_subsystem.drawio.svg)