# Overview

Maze Master is a Python-based puzzle game built with Pygame. The game appears to be in early development stages, featuring a title screen with a play button and basic game window initialization. The project follows a modular structure with organized asset directories for images and sounds, suggesting it will expand into a full maze-solving or maze-generation game.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Game Engine Architecture
- **Framework**: Built on Pygame for 2D game development and rendering
- **Main Game Loop**: Centralized Game class managing the primary game loop with event handling, screen updates, and frame rate control
- **Screen Management**: Fixed resolution display (1280x720) with proper window initialization and icon setup
- **Event System**: Standard Pygame event handling for user input (mouse clicks, window close events)

## Code Organization
- **Modular Structure**: Object-oriented design with separate classes for different game components
- **Asset Management**: Organized directory structure separating code, data, images, and sounds
- **Constants**: Centralized configuration for screen dimensions and frame rate

## File Structure
- **main.py**: Entry point containing core game logic and initialization
- **assets/**: Resource directory for game assets
  - **images/**: Graphics and sprites (includes maze_icon.png)
  - **sounds/**: Audio files for game sounds
- **data/**: Designated for game data files

## Current Implementation
- **Title Screen System**: Basic title screen with interactive play button
- **Mouse Input**: Mouse position tracking and click detection
- **Display Management**: Proper window setup with custom icon and title

# External Dependencies

## Core Dependencies
- **Pygame**: Primary game development framework for graphics, input handling, and game loop management
- **Python Standard Library**: 
  - `sys` for system operations
  - `random` for randomization (likely for maze generation)
  - `os` for file path operations and asset loading

## Asset Requirements
- **Image Assets**: PNG format images stored in assets/images/
- **Audio Assets**: Sound files stored in assets/sounds/ (format not specified)
- **No Database**: Currently no persistent data storage implemented
- **No Network Dependencies**: Standalone single-player game architecture