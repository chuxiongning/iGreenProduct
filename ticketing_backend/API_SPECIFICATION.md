# iGreen Ticketing System - API Specification

## 1. Authentication APIs

### 1.1 Login
- **Endpoint**: `POST /api/auth/login`
- **Request Body**:
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "user": {
      "id": "string",
      "name": "string",
      "username": "string",
      "email": "string",
      "role": "admin | engineer | manager",
      "groupId": "string | null",
      "groupName": "string | null"
    },
    "token": "string"
  }
  ```

### 1.2 Register
- **Endpoint**: `POST /api/auth/register`
- **Request Body**:
  ```json
  {
    "name": "string",
    "email": "string",
    "password": "string",
    "role": "admin | engineer | manager",
    "username": "string"
  }
  ```
- **Response**:
  ```json
  {
    "user": {
      "id": "string",
      "name": "string",
      "username": "string",
      "email": "string",
      "role": "string"
    },
    "token": "string"
  }
  ```

### 1.3 Logout
- **Endpoint**: `POST /api/auth/logout`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{ "message": "Logged out successfully" }`

---

## 2. Tickets APIs

### 2.1 Get All Tickets
- **Endpoint**: `GET /api/tickets`
- **Headers**: `Authorization: Bearer <token>`
- **Query Parameters** (optional):
  - `status`: TicketStatus
  - `priority`: Priority
  - `assignedTo`: string
  - `createdBy`: string
  - `type`: TicketType
- **Response**: `Array<Ticket>`

### 2.2 Get Ticket by ID
- **Endpoint**: `GET /api/tickets/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `Ticket`

### 2.3 Create Ticket
- **Endpoint**: `POST /api/tickets`
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
  ```json
  {
    "title": "string",
    "description": "string",
    "templateId": "string",
    "type": "planned | preventive | corrective | problem",
    "site": "string (optional)",
    "priority": "P1 | P2 | P3 | P4 (optional)",
    "assignedTo": "string",
    "dueDate": "ISO datetime string"
  }
  ```
- **Response**: `Ticket`

### 2.4 Update Ticket
- **Endpoint**: `PUT /api/tickets/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**: Partial<Ticket>
- **Response**: `Ticket`

### 2.5 Delete Ticket
- **Endpoint**: `DELETE /api/tickets/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{ "message": "Ticket deleted" }`

### 2.6 Accept Ticket
- **Endpoint**: `POST /api/tickets/{id}/accept`
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
  ```json
  {
    "comment": "string (optional)"
  }
  ```
- **Response**: `Ticket`

### 2.7 Decline Ticket
- **Endpoint**: `POST /api/tickets/{id}/decline`
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
  ```json
  {
    "reason": "string"
  }
  ```
- **Response**: `Ticket`

### 2.8 Cancel Ticket
- **Endpoint**: `POST /api/tickets/{id}/cancel`
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
  ```json
  {
    "reason": "string"
  }
  ```
- **Response**: `Ticket`

---

## 3. Templates APIs

### 3.1 Get All Templates
- **Endpoint**: `GET /api/templates`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `Array<Template>`

### 3.2 Get Template by ID
- **Endpoint**: `GET /api/templates/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `Template`

### 3.3 Create Template
- **Endpoint**: `POST /api/templates`
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string",
    "steps": [
      {
        "name": "string",
        "description": "string",
        "order": "number",
        "fields": [
          {
            "name": "string",
            "type": "text | number | date | location | photo | signature | faceRecognition",
            "required": "boolean"
          }
        ]
      }
    ]
  }
  ```
- **Response**: `Template`

### 3.4 Update Template
- **Endpoint**: `PUT /api/templates/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**: Partial<Template>
- **Response**: `Template`

### 3.5 Delete Template
- **Endpoint**: `DELETE /api/templates/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{ "message": "Template deleted" }`

---

## 4. Users APIs

### 4.1 Get All Users
- **Endpoint**: `GET /api/users`
- **Headers**: `Authorization: Bearer <token>`
- **Query Parameters** (optional):
  - `role`: string
  - `groupId`: string
  - `status`: "active | inactive"
- **Response**: `Array<User>`

### 4.2 Get User by ID
- **Endpoint**: `GET /api/users/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `User`

### 4.3 Update User Profile
- **Endpoint**: `PUT /api/users/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
  ```json
  {
    "name": "string (optional)",
    "username": "string (optional)",
    "groupId": "string (optional)",
    "status": "active | inactive (optional)"
  }
  ```
- **Response**: `User`

### 4.4 Create User
- **Endpoint**: `POST /api/users`
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
  ```json
  {
    "name": "string",
    "username": "string",
    "email": "string",
    "password": "string",
    "role": "admin | engineer | manager",
    "groupId": "string (optional)"
  }
  ```
- **Response**: `User`

### 4.5 Delete User
- **Endpoint**: `DELETE /api/users/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{ "message": "User deleted" }`

---

## 5. Groups APIs

### 5.1 Get All Groups
- **Endpoint**: `GET /api/groups`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `Array<Group>`

### 5.2 Get Group by ID
- **Endpoint**: `GET /api/groups/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `Group`

### 5.3 Create Group
- **Endpoint**: `POST /api/groups`
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string",
    "tags": ["string"],
    "status": "active | inactive"
  }
  ```
- **Response**: `Group`

### 5.4 Update Group
- **Endpoint**: `PUT /api/groups/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**: Partial<Group>
- **Response**: `Group`

### 5.5 Delete Group
- **Endpoint**: `DELETE /api/groups/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{ "message": "Group deleted" }`

---

## 6. Sites APIs

### 6.1 Get All Sites
- **Endpoint**: `GET /api/sites`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `Array<Site>`

### 6.2 Get Site by ID
- **Endpoint**: `GET /api/sites/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `Site`

### 6.3 Create Site
- **Endpoint**: `POST /api/sites`
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
  ```json
  {
    "name": "string",
    "address": "string",
    "level": "normal | vip | string",
    "status": "online | offline | underConstruction"
  }
  ```
- **Response**: `Site`

### 6.4 Update Site
- **Endpoint**: `PUT /api/sites/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**: Partial<Site>
- **Response**: `Site`

### 6.5 Delete Site
- **Endpoint**: `DELETE /api/sites/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{ "message": "Site deleted" }`

---

## 7. SLA Configurations APIs

### 7.1 Get All SLA Configs
- **Endpoint**: `GET /api/sla-configs`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `Array<SLAConfig>`

### 7.2 Get SLA Config by Priority
- **Endpoint**: `GET /api/sla-configs/{priority}`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `SLAConfig`

### 7.3 Create/Update SLA Config
- **Endpoint**: `POST /api/sla-configs`
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
  ```json
  {
    "priority": "P1 | P2 | P3 | P4",
    "responseTime": "number (minutes)",
    "resolutionTime": "number (minutes)"
  }
  ```
- **Response**: `SLAConfig`

---

## 8. Problem Types APIs

### 8.1 Get All Problem Types
- **Endpoint**: `GET /api/problem-types`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `Array<ProblemType>`

### 8.2 Create Problem Type
- **Endpoint**: `POST /api/problem-types`
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string"
  }
  ```
- **Response**: `ProblemType`

### 8.3 Update Problem Type
- **Endpoint**: `PUT /api/problem-types/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**: Partial<ProblemType>
- **Response**: `ProblemType`

### 8.4 Delete Problem Type
- **Endpoint**: `DELETE /api/problem-types/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{ "message": "Problem type deleted" }`

---

## 9. Site Level Configurations APIs

### 9.1 Get All Site Level Configs
- **Endpoint**: `GET /api/site-level-configs`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `Array<SiteLevelConfig>`

### 9.2 Create Site Level Config
- **Endpoint**: `POST /api/site-level-configs`
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string",
    "slaMultiplier": "number"
  }
  ```
- **Response**: `SiteLevelConfig`

### 9.3 Update Site Level Config
- **Endpoint**: `PUT /api/site-level-configs/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**: Partial<SiteLevelConfig>
- **Response**: `SiteLevelConfig`

### 9.4 Delete Site Level Config
- **Endpoint**: `DELETE /api/site-level-configs/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{ "message": "Site level config deleted" }`

---

## 10. File Upload APIs

### 10.1 Upload File
- **Endpoint**: `POST /api/files/upload`
- **Headers**:
  - `Authorization: Bearer <token>`
  - `Content-Type: multipart/form-data`
- **Request Body**: FormData with:
  - `file`: File
  - `fieldType`: "photo | signature | faceRecognition"
- **Response**:
  ```json
  {
    "id": "string",
    "url": "string",
    "name": "string",
    "type": "string",
    "size": "number"
  }
  ```

### 10.2 Delete File
- **Endpoint**: `DELETE /api/files/{id}`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{ "message": "File deleted" }`

---

## 11. Face Recognition APIs

### 11.1 Verify Face
- **Endpoint**: `POST /api/face-recognition/verify`
- **Headers**:
  - `Authorization: Bearer <token>`
  - `Content-Type: multipart/form-data`
- **Request Body**: FormData with:
  - `image`: File
  - `userId`: string (optional, for matching against specific user)
- **Response**:
  ```json
  {
    "verified": "boolean",
    "confidence": "number (0-1)",
    "message": "string"
  }
  ```

---

## Data Models

### Ticket
```typescript
{
  id: string
  title: string
  description: string
  templateId: string
  templateName: string
  type: "planned" | "preventive" | "corrective" | "problem"
  site?: string
  status: "open" | "accepted" | "inProgress" | "closed" | "onHold" | "cancelled" | "submitted"
  priority?: "P1" | "P2" | "P3" | "P4"
  assignedTo: string
  assignedToName: string
  createdBy: string
  createdByName: string
  createdAt: Date
  dueDate: Date
  completedSteps: string[]
  stepData: Record<string, any>
  accepted?: boolean
  acceptedAt?: Date
  departureAt?: Date
  departurePhoto?: string
  arrivalAt?: Date
  arrivalPhoto?: string
  completionPhoto?: string
  cause?: string
  solution?: string
  comments: TicketComment[]
  relatedTicketIds?: string[]
}
```

### Template
```typescript
{
  id: string
  name: string
  description: string
  steps: TemplateStep[]
  createdAt: Date
  updatedAt: Date
}
```

### User
```typescript
{
  id: string
  name: string
  username: string
  email: string
  role: "admin" | "engineer" | "manager"
  groupId?: string
  groupName?: string
  status?: "active" | "inactive"
  createdAt?: Date
}
```

### Group
```typescript
{
  id: string
  name: string
  description: string
  tags: string[]
  status: "active" | "inactive"
  createdAt: Date
  updatedAt: Date
}
```

### Site
```typescript
{
  id: string
  name: string
  address: string
  level: "normal" | "vip" | string
  status: "online" | "offline" | "underConstruction"
  createdAt: Date
  updatedAt: Date
}
```
