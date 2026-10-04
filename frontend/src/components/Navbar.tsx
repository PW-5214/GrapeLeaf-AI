import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Grape, Menu, X, FileText, FlaskConical, BookOpen, Info, Home } from 'lucide-react';

export const Navbar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const navLinks = [
    { name: 'Home', path: '/', icon: Home },
    { name: 'Analyze Sample', path: '/analyze', icon: FlaskConical },
    { name: 'My Report', path: '/report', icon: FileText },
    { name: 'Reference Standards', path: '/standards', icon: BookOpen },
    { name: 'About GrapeLeaf AI', path: '/about', icon: Info },
  ];

  const isActive = (path: string) => {
    if (path === '/' && location.pathname === '/') return true;
    if (path !== '/' && location.pathname.startsWith(path)) return true;
    return false;
  };

  return (
    <header className="sticky top-0 z-50 bg-[#54245F] text-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo */}
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center border border-white/20 group-hover:bg-white/20 transition-all">
              <Grape className="w-6 h-6 text-[#98D65F] group-hover:scale-105 transition-transform" />
            </div>
            <div>
              <span className="font-bold text-lg sm:text-xl tracking-tight text-white flex items-center gap-1">
                GrapeLeaf <span className="text-[#98D65F] text-sm sm:text-base font-semibold px-1.5 py-0.2 rounded bg-white/10">AI</span>
              </span>
              <p className="text-[10px] text-white/75 tracking-wider uppercase font-medium">
                Petiole & Leaf Advisory
              </p>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-1.5">
            {navLinks.map((link) => {
              const Icon = link.icon;
              const active = isActive(link.path);
              return (
                <Link
                  key={link.path}
                  to={link.path}
                  className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    active
                      ? 'bg-white/20 text-white shadow-inner font-semibold'
                      : 'text-white/80 hover:bg-white/10 hover:text-white'
                  }`}
                >
                  <Icon size={16} className={active ? 'text-[#98D65F]' : 'text-white/70'} />
                  <span>{link.name}</span>
                </Link>
              );
            })}
            <Link
              to="/analyze"
              className="ml-3 px-4 py-2 rounded-lg text-sm font-semibold bg-[#4F772D] hover:bg-[#3f6024] text-white shadow transition-all flex items-center gap-1.5 border border-white/20"
            >
              <FlaskConical size={16} />
              <span>New Analysis</span>
            </Link>
          </nav>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="p-2 rounded-lg text-white/80 hover:text-white hover:bg-white/10 focus:outline-none"
              aria-label="Toggle navigation menu"
            >
              {isOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile dropdown */}
      {isOpen && (
        <div className="md:hidden bg-[#431c4c] border-t border-white/10 px-4 pt-2 pb-4 space-y-1">
          {navLinks.map((link) => {
            const Icon = link.icon;
            const active = isActive(link.path);
            return (
              <Link
                key={link.path}
                to={link.path}
                onClick={() => setIsOpen(false)}
                className={`flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm font-medium ${
                  active
                    ? 'bg-white/20 text-white font-semibold'
                    : 'text-white/80 hover:bg-white/10 hover:text-white'
                }`}
              >
                <Icon size={18} className={active ? 'text-[#98D65F]' : 'text-white/70'} />
                <span>{link.name}</span>
              </Link>
            );
          })}
        </div>
      )}
    </header>
  );
};
