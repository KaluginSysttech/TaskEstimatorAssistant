# Sprint S3 Quick Start Guide

## 🚀 Quick Start

### Step 1: Start the Mock API
The dashboard needs the backend Mock API to display data.

```bash
# From the project root
cd C:\Users\v.kalugin\Desktop\TEARepo
make run  # or python src/api_main.py
```

The Mock API should be running at: `http://localhost:8001`

### Step 2: Start the Frontend
Open a new terminal and start the Next.js development server.

```bash
cd C:\Users\v.kalugin\Desktop\TEARepo\frontend
pnpm run dev
```

### Step 3: Open the Dashboard
Open your browser and navigate to:
```
http://localhost:3000
```

## ✨ What You'll See

### Main Dashboard Features

1. **Collapsible Sidebar (Hidden by Default)**
   - Click the hamburger menu (☰) in the top-left to open
   - Shows TEA branding and navigation
   - Click outside or X button to close

2. **Header Bar**
   - Menu button (☰) - Opens sidebar
   - Period selector - Switch between Day/Week/Month
   - Refresh button (⟳) - Reload data
   - GitHub button - Links to repository

3. **KPI Cards (Always Visible)**
   - Total Conversations
   - Active Users
   - Average Conversation Length
   - Growth Rate
   - Each with trend indicators and change percentages

4. **Activity Chart**
   - Beautiful area chart showing activity over time
   - Responsive and interactive
   - Period-aware (changes based on selected period)

5. **Collapsible Tables (Hidden by Default)**
   - **Recent Conversations**
     - Click "Show" to expand
     - Shows last conversations with user names, times, message counts
   - **Top Users**
     - Click "Show" to expand
     - Shows ranked list of most active users

## 🎨 UI Features to Try

### Sidebar
- Open/close the sidebar with the menu button
- Notice the smooth slide animation
- Try on mobile view (resize browser) - backdrop overlay appears
- State is saved in localStorage

### Tables
- Click "Show" on Recent Conversations
- Click "Show" on Top Users
- Both tables are hidden by default to keep the dashboard clean
- Click "Hide" to collapse them again

### Period Switching
- Change the period selector (Day/Week/Month)
- Watch the data update
- Notice the chart description changes

### Dark Theme
- Enjoy the high-contrast dark theme
- All text is clearly readable
- Charts use contrasting colors
- Hover effects on interactive elements

## 🧪 Test the Features

1. **Test Sidebar**:
   - Click hamburger menu → Sidebar opens
   - Click outside → Sidebar closes
   - Click menu again → Sidebar reopens

2. **Test Period Selection**:
   - Select "Day" → Data updates
   - Select "Week" → Data updates
   - Select "Month" → Data updates

3. **Test Refresh**:
   - Click refresh button (⟳)
   - Watch loading spinner
   - Data reloads

4. **Test GitHub Link**:
   - Click GitHub icon
   - Opens repository in new tab
   - Link: https://github.com/KaluginSysttech/TaskEstimatorAssistant

5. **Test Collapsible Tables**:
   - Click "Show" on Recent Conversations → Table expands
   - Click "Hide" → Table collapses
   - Repeat for Top Users

## 📱 Responsive Design

Try resizing your browser to see responsive behavior:
- **Mobile** (< 640px): Compact layout, sidebar with backdrop
- **Tablet** (640px - 1024px): 2-column grids
- **Desktop** (> 1024px): Full 4-column layout

## 🐛 Troubleshooting

### Mock API Not Running
**Error**: Network error or "Unable to connect to API"
**Solution**: Make sure the Mock API is running at `http://localhost:8001`

```bash
cd C:\Users\v.kalugin\Desktop\TEARepo
python src/api_main.py
```

### Port Already in Use
**Error**: "Port 3000 is already in use"
**Solution**: Either stop the other process or use a different port:

```bash
pnpm run dev -- -p 3001
```

### Dependencies Issue
**Error**: Module not found
**Solution**: Reinstall dependencies:

```bash
cd frontend
rm -rf node_modules
rm pnpm-lock.yaml
pnpm install
```

## 📸 Screenshots

When running, you should see:
- Dark themed dashboard
- 4 KPI cards at the top
- Large activity chart in the middle
- Two collapsible sections at the bottom
- Smooth animations on all interactions

## 🎯 Key Interactions

| Action | Expected Result |
|--------|----------------|
| Open sidebar | Sidebar slides in from left |
| Click backdrop | Sidebar closes |
| Change period | Chart updates, metrics recalculate |
| Click refresh | Loading spinner → Data updates |
| Click GitHub | New tab opens with repository |
| Show table | Table smoothly expands with data |
| Hide table | Table collapses |
| Hover card | Subtle highlight effect |
| Hover button | Color change |

## ✅ Success Checklist

- [ ] Mock API is running (http://localhost:8001)
- [ ] Frontend is running (http://localhost:3000)
- [ ] Dashboard loads without errors
- [ ] Sidebar is hidden by default
- [ ] Can open/close sidebar
- [ ] GitHub button works
- [ ] Period selector changes data
- [ ] Refresh button works
- [ ] Tables are hidden by default
- [ ] Can expand/collapse tables
- [ ] Chart displays properly
- [ ] All text is readable (high contrast)
- [ ] Hover effects work

## 🎉 You're Done!

Your Sprint S3 Dashboard is now complete and running! Enjoy exploring the modern, professional UI.

For any issues or questions, refer to:
- `SPRINT_S3_SUMMARY.md` - Full implementation details
- `frontend/doc/front-vision.md` - Architecture and principles
- Component source code in `frontend/components/`

---

**Happy Dashboard-ing! 📊**

