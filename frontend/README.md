# Exoskeleton Dashboard Frontend

React + TypeScript dashboard for real-time exoskeleton telemetry visualization.

## Requirements

- Node.js 18 or higher
- npm 9 or higher

## Setup

### Install Dependencies

```bash
npm install
```

### Run Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build for Production

```bash
npm run build
```

Build output will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Development

### Linting

```bash
npm run lint
```

### Formatting

```bash
npm run format
```

## Technology Stack

- **React 19** - UI framework
- **TypeScript 5** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first styling
- **Recharts** - Real-time charting library
- **ESLint + Prettier** - Code quality

## Project Structure

```
frontend/
├── src/
│   ├── components/     # React components (coming soon)
│   ├── hooks/          # Custom React hooks (coming soon)
│   ├── types/          # TypeScript type definitions (coming soon)
│   ├── App.tsx         # Main application component
│   ├── main.tsx        # Application entry point
│   └── index.css       # Global styles with Tailwind
├── index.html          # HTML entry point
├── vite.config.ts      # Vite configuration
├── tsconfig.json       # TypeScript configuration
├── tailwind.config.js  # Tailwind CSS configuration
├── eslint.config.js    # ESLint configuration
└── package.json        # Dependencies and scripts
```
