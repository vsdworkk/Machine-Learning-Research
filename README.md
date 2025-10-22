# FEG Machine Learning

A modern web application built with Next.js, featuring machine learning capabilities.

## Tech Stack

- **Frontend**: Next.js, Tailwind CSS, Shadcn/ui, Framer Motion
- **Backend**: Postgres, Supabase, Drizzle ORM, Server Actions
- **Authentication**: Clerk
- **Payments**: Stripe
- **Deployment**: Vercel

## Getting Started

First, install the dependencies:

```bash
npm install
# or
yarn install
# or
pnpm install
```

Then, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Environment Variables

Copy `.env.example` to `.env.local` and fill in your environment variables.

## Project Structure

- `actions/` - Server actions
- `app/` - Next.js app router
- `components/` - Shared components
- `db/` - Database schemas and configuration
- `lib/` - Library code and utilities
- `types/` - TypeScript type definitions

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.
