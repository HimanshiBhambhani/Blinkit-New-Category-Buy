// Static export for GitHub Pages is toggled with STATIC_EXPORT=1.
// Served from https://<user>.github.io/Blinkit-New-Category-Buy/
const isStaticExport = process.env.STATIC_EXPORT === "1";
const repoBasePath = "/Blinkit-New-Category-Buy";

/** @type {import('next').NextConfig} */
const nextConfig = {
  ...(isStaticExport
    ? {
        output: "export",
        basePath: repoBasePath,
        assetPrefix: `${repoBasePath}/`,
        trailingSlash: true,
        env: { NEXT_PUBLIC_BASE_PATH: repoBasePath },
      }
    : {}),
  images: {
    unoptimized: isStaticExport,
    remotePatterns: [
      {
        protocol: "https",
        hostname: "lh3.googleusercontent.com",
      },
    ],
  },
  webpack: (config, { dev }) => {
    if (dev) {
      config.watchOptions = {
        poll: 1000,
        aggregateTimeout: 300,
      };
    }
    return config;
  },
};

export default nextConfig;
