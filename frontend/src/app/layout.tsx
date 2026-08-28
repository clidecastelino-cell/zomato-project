import type { Metadata } from 'next';
import { Inter, Outfit } from 'next/font/google';
import './globals.css';
import Sidebar from '@/components/Sidebar';
import MobileHeader from '@/components/MobileHeader';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });
const outfit = Outfit({ subsets: ['latin'], variable: '--font-outfit' });

export const metadata: Metadata = {
  title: 'Lumiere AI - Premium Concierge',
  description: 'AI-Powered Restaurant Recommender based on Zomato data',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} ${outfit.variable}`}>
      <head>
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
        />
      </head>
      <body className="flex h-screen overflow-hidden font-body-md text-body-md selection:bg-primary-container selection:text-white">
        <Sidebar />
        <MobileHeader />
        
        <main className="flex-1 ml-0 md:ml-[280px] mt-[72px] md:mt-0 p-container-padding-mobile md:p-container-padding-desktop overflow-y-auto relative scroll-smooth">
          {/* Ambient Background Glow */}
          <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-primary/10 rounded-full blur-[120px] pointer-events-none -z-10"></div>
          <div className="absolute bottom-0 left-1/4 w-[400px] h-[400px] bg-tertiary-container/10 rounded-full blur-[100px] pointer-events-none -z-10"></div>
          
          <div className="max-w-[1000px] mx-auto space-y-stack-lg">
            {children}
          </div>
        </main>
      </body>
    </html>
  );
}
