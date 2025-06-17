# FLAMES Game – Logic

The application is a GUI-based FLAMES game which is implemented under Python `tkinter`. It updates the traditional paper game to a reactive interface and personal choices, as well as indicating a continuing history of the session.

---

##  Features Overview

- **User-Friendly GUI**: Responsive and maximized interface using `tkinter`.
- **Customizable FLAMES Categories**: Users can define their own relationship categories.
- **Real-Time Input Validation**: Ensures names contain only letters and aren’t identical.
- **Dark/Light Theme Toggle**: Easily switch between themes for better UX.
- **Result Animation**: FLAMES result is displayed with animated scaling and color transition.
- **History Management**: Tracks all game results with timestamps.
- **Import/Export History**: Save session data or load past results.
- **Keyboard Shortcuts**: 
  - `Enter` to calculate
  - `Ctrl+C` to clear
  - `Ctrl+T` to toggle theme

---

##  Core Logic

### Input Validation

- Ensures both names are:
  - Non-empty
  - Contain only letters and spaces
  - Not the same (case-insensitive)

### FLAMES Algorithm

1. Remove all common characters between the two names.
2. Count the remaining characters.
3. Use that count to cyclically eliminate categories from the list until one remains.
4. The final category is the relationship result.

### Customization Logic

- Categories can be updated by users via a popup window.
- Validation checks ensure each new category:
  - Is not empty
  - Contains only alphabets/spaces
  - Is unique

### Theme Support

- Uses a dictionary of color schemes.
- Recursively updates colors for all widgets using the selected theme.

