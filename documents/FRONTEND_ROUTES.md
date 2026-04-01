# 🌐 Propertism Frontend Routes

**Framework**: React Router 6  
**Authentication**: Protected routes with role-based access

---

## 📚 Route Structure

```
/
├── /                           # Public
├── /properties                 # Public
├── /properties/:id             # Public
├── /contact                    # Public
├── /about                      # Public
├── /services                   # Public
├── /construction-updates       # Public
├── /faq                        # Public
├── /login                      # Public
├── /register                   # Public
├── /forgot-password            # Public
├── /reset-password/:token      # Public
│
├── /dashboard                  # User
├── /dashboard/my-inquiries     # User
├── /dashboard/my-maintenance   # User
├── /dashboard/my-tickets       # User
├── /dashboard/profile          # User
│
└── /admin                      # Admin
    ├── /admin/properties       # Admin
    ├── /admin/inquiries        # Admin
    ├── /admin/maintenance      # Admin
    ├── /admin/tickets          # Admin
    ├── /admin/users            # Admin
    ├── /admin/subscriptions    # Admin
    └── /admin/settings         # Admin
```

---

## 📋 Route Details

### Public Routes

#### `/` - Homepage
**Component**: `pages/HomePage.tsx`  
**Public**: Yes  
**Description**: Main landing page with hero section, featured properties, services overview

**Features**:
- Hero banner with call-to-action
- Featured properties section
- Services overview
- Contact information
- Quick inquiry form

---

#### `/properties` - Property Listings
**Component**: `pages/PropertyListPage.tsx`  
**Public**: Yes  
**Description**: Browse all properties with filters

**Features**:
- Property filters (type, price, location, bedrooms)
- Responsive property cards
- Pagination
- Search functionality

**Query Parameters**:
- `type` - Property type filter
- `minPrice` - Minimum price
- `maxPrice` - Maximum price
- `location` - Location filter
- `bedrooms` - Bedroom count filter

---

#### `/properties/:id` - Property Details
**Component**: `pages/PropertyDetailPage.tsx`  
**Public**: Yes  
**Description**: Detailed view of a specific property

**Features**:
- Property gallery
- Detailed information
- Contact form for inquiries
- Similar properties section

---

#### `/contact` - Contact Page
**Component**: `pages/ContactPage.tsx`  
**Public**: Yes  
**Description**: Contact form and company information

**Features**:
- Contact form (name, email, phone, subject, message)
- Company address and contact info
- Map integration (optional)

---

#### `/about` - About Us
**Component**: `pages/AboutPage.tsx`  
**Public**: Yes  
**Description**: Company information and team

**Features**:
- Company history
- Mission and values
- Team members
- Contact information

---

#### `/services` - Services
**Component**: `pages/ServicesPage.tsx`  
**Public**: Yes  
**Description**: Services overview

**Features**:
- Property management services
- Rental assistance
- Industrial land services
- Buy/sell assistance

---

#### `/construction-updates` - Construction Updates
**Component**: `pages/ConstructionUpdatesPage.tsx`  
**Public**: Yes  
**Description**: Real-time construction progress

**Features**:
- Timeline of updates
- Images and descriptions
- Property filtering

---

#### `/faq` - FAQ
**Component**: `pages/FAQPage.tsx`  
**Public**: Yes  
**Description**: Frequently asked questions

**Features**:
- Accordion-style FAQ
- Categories
- Search functionality

---

#### `/login` - Login
**Component**: `pages/LoginPage.tsx`  
**Public**: Yes  
**Description**: User login page

**Features**:
- Email/password login
- "Remember me" checkbox
- Link to register
- Link to forgot password

---

#### `/register` - Register
**Component**: `pages/RegisterPage.tsx`  
**Public**: Yes  
**Description**: User registration page

**Features**:
- Registration form (email, password, name, phone)
- Form validation
- Terms and conditions

---

#### `/forgot-password` - Forgot Password
**Component**: `pages/ForgotPasswordPage.tsx`  
**Public**: Yes  
**Description**: Password reset request

**Features**:
- Email input
- Submit button
- Success message

---

#### `/reset-password/:token` - Reset Password
**Component**: `pages/ResetPasswordPage.tsx`  
**Public**: Yes  
**Description**: Password reset form

**Features**:
- New password input
- Confirm password input
- Submit button

---

### User Routes (Authenticated)

#### `/dashboard` - User Dashboard
**Component**: `pages/DashboardPage.tsx`  
**Public**: No  
**Roles**: user, admin  
**Description**: User's main dashboard

**Features**:
- Welcome message
- Quick stats (inquiries, maintenance, tickets)
- Recent activity
- Quick links

---

#### `/dashboard/my-inquiries` - My Inquiries
**Component**: `pages/MyInquiriesPage.tsx`  
**Public**: No  
**Roles**: user, admin  
**Description**: User's property inquiries

**Features**:
- List of all inquiries
- Status badges
- Property information
- Filter by status

---

#### `/dashboard/my-maintenance` - My Maintenance Requests
**Component**: `pages/MyMaintenancePage.tsx`  
**Public**: No  
**Roles**: user, admin  
**Description**: User's maintenance requests

**Features**:
- List of maintenance requests
- Priority badges
- Status tracking
- Create new request button

---

#### `/dashboard/my-tickets` - My Support Tickets
**Component**: `pages/MyTicketsPage.tsx`  
**Public**: No  
**Roles**: user, admin  
**Description**: User's support tickets

**Features**:
- List of support tickets
- Priority badges
- Status tracking
- Create new ticket button

---

#### `/dashboard/profile` - User Profile
**Component**: `pages/ProfilePage.tsx`  
**Public**: No  
**Roles**: user, admin  
**Description**: User profile management

**Features**:
- Profile information
- Edit profile form
- Change password form
- Delete account option

---

### Admin Routes (Admin Only)

#### `/admin` - Admin Dashboard
**Component**: `pages/AdminDashboardPage.tsx`  
**Public**: No  
**Roles**: admin  
**Description**: Admin's main dashboard

**Features**:
- Admin navigation
- Quick stats (users, properties, inquiries, tickets)
- Recent activity
- Quick actions

---

#### `/admin/properties` - Property Management
**Component**: `pages/AdminPropertiesPage.tsx`  
**Public**: No  
**Roles**: admin  
**Description**: Admin property management

**Features**:
- Property list table
- Create property button
- Edit/Delete actions
- Filter and search
- Image upload

---

#### `/admin/inquiries` - Inquiry Management
**Component**: `pages/AdminInquiriesPage.tsx`  
**Public**: No  
**Roles**: admin  
**Description**: Admin inquiry management

**Features**:
- Inquiry list table
- Status management
- View details
- Export functionality

---

#### `/admin/maintenance` - Maintenance Management
**Component**: `pages/AdminMaintenancePage.tsx`  
**Public**: No  
**Roles**: admin  
**Description**: Admin maintenance request management

**Features**:
- Request list table
- Status management
- Priority management
- Assign to staff

---

#### `/admin/tickets` - Ticket Management
**Component**: `pages/AdminTicketsPage.tsx`  
**Public**: No  
**Roles**: admin  
**Description**: Admin support ticket management

**Features**:
- Ticket list table
- Status management
- Comment functionality
- Priority management

---

#### `/admin/users` - User Management
**Component**: `pages/AdminUsersPage.tsx`  
**Public**: No  
**Roles**: admin  
**Description**: Admin user management

**Features**:
- User list table
- Edit user functionality
- Make/Remove Admin
- Delete user
- View user details

---

#### `/admin/subscriptions` - Subscription Management
**Component**: `pages/AdminSubscriptionsPage.tsx`  
**Public**: No  
**Roles**: admin  
**Description**: Admin subscription management

**Features**:
- Subscription list table
- Export functionality
- Filter by status

---

#### `/admin/settings` - Admin Settings
**Component**: `pages/AdminSettingsPage.tsx`  
**Public**: No  
**Roles**: admin  
**Description**: Admin site settings

**Features**:
- Site configuration
- Email settings
- Social media links
- Contact information

---

## 🔐 Route Protection

### Authentication Guard

```typescript
// src/hooks/useAuth.ts
const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // Check if user is authenticated
  const isAuthenticated = !!user;

  // Check if user has specific role
  const hasRole = (role: string) => user?.role === role;

  return { user, loading, isAuthenticated, hasRole };
};
```

### Protected Route Component

```typescript
// src/components/ProtectedRoute.tsx
interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRole?: string;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  children, 
  requiredRole 
}) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <Spinner />;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (requiredRole && user.role !== requiredRole) {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
};
```

### Route Configuration

```typescript
// src/App.tsx
const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<HomePage />} />
        <Route path="/properties" element={<PropertyListPage />} />
        <Route path="/properties/:id" element={<PropertyDetailPage />} />
        <Route path="/contact" element={<ContactPage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/services" element={<ServicesPage />} />
        <Route path="/construction-updates" element={<ConstructionUpdatesPage />} />
        <Route path="/faq" element={<FAQPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/reset-password/:token" element={<ResetPasswordPage />} />

        {/* User Routes */}
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        } />
        <Route path="/dashboard/my-inquiries" element={
          <ProtectedRoute>
            <MyInquiriesPage />
          </ProtectedRoute>
        } />
        <Route path="/dashboard/my-maintenance" element={
          <ProtectedRoute>
            <MyMaintenancePage />
          </ProtectedRoute>
        } />
        <Route path="/dashboard/my-tickets" element={
          <ProtectedRoute>
            <MyTicketsPage />
          </ProtectedRoute>
        } />
        <Route path="/dashboard/profile" element={
          <ProtectedRoute>
            <ProfilePage />
          </ProtectedRoute>
        } />

        {/* Admin Routes */}
        <Route path="/admin" element={
          <ProtectedRoute requiredRole="admin">
            <AdminDashboardPage />
          </ProtectedRoute>
        } />
        <Route path="/admin/properties" element={
          <ProtectedRoute requiredRole="admin">
            <AdminPropertiesPage />
          </ProtectedRoute>
        } />
        <Route path="/admin/inquiries" element={
          <ProtectedRoute requiredRole="admin">
            <AdminInquiriesPage />
          </ProtectedRoute>
        } />
        <Route path="/admin/maintenance" element={
          <ProtectedRoute requiredRole="admin">
            <AdminMaintenancePage />
          </ProtectedRoute>
        } />
        <Route path="/admin/tickets" element={
          <ProtectedRoute requiredRole="admin">
            <AdminTicketsPage />
          </ProtectedRoute>
        } />
        <Route path="/admin/users" element={
          <ProtectedRoute requiredRole="admin">
            <AdminUsersPage />
          </ProtectedRoute>
        } />
        <Route path="/admin/subscriptions" element={
          <ProtectedRoute requiredRole="admin">
            <AdminSubscriptionsPage />
          </ProtectedRoute>
        } />
        <Route path="/admin/settings" element={
          <ProtectedRoute requiredRole="admin">
            <AdminSettingsPage />
          </ProtectedRoute>
        } />

        {/* 404 Route */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  );
};
```

---

## 📝 Notes

- All routes use React Router 6
- Protected routes use role-based access control
- Admin routes require `admin` role
- User routes are accessible to both `user` and `admin` roles
- Public routes are accessible to everyone
- 404 page for undefined routes

---

**Last Updated**: February 22, 2026
