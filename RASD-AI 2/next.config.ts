import type { NextConfig } from 'next';
const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  async headers() { return [{source: '/:path*', headers: [
    {key: 'X-Content-Type-Options', value: 'nosniff'},
    {key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin'},
    {key: 'X-Frame-Options', value: 'DENY'},
    {key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()'},
    {key: 'Content-Security-Policy', value: "default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; form-action 'self'; img-src 'self' blob: data:; connect-src 'self'; font-src 'self' https://fonts.gstatic.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; script-src 'self' 'unsafe-inline' 'unsafe-eval'"}
  ]}]; }
};
export default nextConfig;
