import { useState } from 'react';
import { useNavigate } from 'react-router';
import { ProductManagement } from './ProductManagement';
import { ClipboardList, Package, LogOut, Sparkles, SlidersHorizontal, Warehouse, KeyRound, UserCog } from 'lucide-react';
import { Button } from './ui/button';
import { NotificationCenter } from './NotificationCenter';
import { useAuth } from '../../lib/auth-context';
import { BrandLogo } from './BrandLogo';
import { InventoryLogPage } from './InventoryLogPage';
import { PortalPasswordResetModal } from './PortalPasswordResetModal';
import { PortalProfileSettingsModal } from './PortalProfileSettingsModal';

export function InventoryStaffLayout() {
  const navigate = useNavigate();
  const [activeView, setActiveView] = useState('product-list');
  const { user, logout } = useAuth();
  const [isPasswordResetOpen, setIsPasswordResetOpen] = useState(false);
  const [isProfileSettingsOpen, setIsProfileSettingsOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const navItems = [
    { id: 'product-list', label: 'Product List', icon: Package },
    { id: 'product-settings', label: 'Product Settings', icon: SlidersHorizontal },
    { id: 'inventory', label: 'Inventory', icon: Warehouse },
    { id: 'inventory-log', label: 'Inventory Log', icon: ClipboardList },
  ];

  const renderContent = () => {
    switch (activeView) {
      case 'product-list':
        return <ProductManagement view="list" onViewChange={(view) => setActiveView(view === 'list' ? 'product-list' : view === 'settings' ? 'product-settings' : 'inventory')} />;
      case 'product-settings':
        return <ProductManagement view="settings" onViewChange={(view) => setActiveView(view === 'list' ? 'product-list' : view === 'settings' ? 'product-settings' : 'inventory')} />;
      case 'inventory':
        return <ProductManagement view="inventory" onViewChange={(view) => setActiveView(view === 'list' ? 'product-list' : view === 'settings' ? 'product-settings' : 'inventory')} />;
      case 'inventory-log':
        return <InventoryLogPage />;
      default:
        return <ProductManagement view="list" onViewChange={(view) => setActiveView(view === 'list' ? 'product-list' : view === 'settings' ? 'product-settings' : 'inventory')} />;
    }
  };

  const activeLabel = navItems.find(item => item.id === activeView)?.label;

  return (
    <div className="flex h-screen bg-[#0E0E12] text-white p-3 gap-3">
      <aside className="w-64 bg-[#16161C] flex flex-col rounded-2xl border border-white/5 overflow-hidden">
        <div className="px-5 pt-5 pb-4 flex items-center gap-3">
          <BrandLogo size="md" />
          <div>
            <h1 className="text-white text-base leading-none">Meryl Shoes</h1>
            <p className="text-[11px] text-white/40 mt-1">Inventory Portal</p>
          </div>
        </div>
        <div className="px-3"><div className="text-[10px] uppercase tracking-wider text-white/30 px-3 py-2">Menu</div></div>
        <nav className="flex-1 px-3 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeView === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveView(item.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all text-sm ${
                  isActive
                    ? 'bg-gradient-to-r from-[#E5202A] to-[#B81820] text-white shadow-lg shadow-red-900/30'
                    : 'text-white/60 hover:bg-white/5 hover:text-white'
                }`}
              >
                <Icon className="w-[18px] h-[18px]" />
                <span>{item.label}</span>
                {isActive && <span className="ml-auto w-1.5 h-1.5 rounded-full bg-[#FFD60A]" />}
              </button>
            );
          })}
        </nav>
        <div className="p-3">
          <div className="rounded-2xl p-4 bg-gradient-to-br from-[#FFD60A] to-[#FFB800] text-[#1A1A22] relative overflow-hidden">
            <Sparkles className="absolute -top-2 -right-2 w-16 h-16 opacity-20" />
            <div className="flex items-center gap-2.5 mb-2 relative z-10">
              <div className="w-8 h-8 rounded-full overflow-hidden border border-[#1A1A22]/30 bg-black/10 flex items-center justify-center shrink-0">
                {user?.avatar_url ? (
                  <img src={user.avatar_url} alt={user.name} className="w-full h-full object-cover" />
                ) : (
                  <span className="text-xs font-bold text-[#1A1A22]">{(user?.name || 'I').charAt(0).toUpperCase()}</span>
                )}
              </div>
              <div className="min-w-0 flex-1">
                <div className="text-[11px] opacity-70 leading-none mb-0.5">Welcome back</div>
                <div className="text-xs leading-tight truncate font-bold">{user?.name || 'Inventory Staff'}</div>
              </div>
            </div>
            <div className="mt-3 flex flex-col gap-1.5 relative z-10">
              <Button
                type="button"
                onClick={() => setIsProfileSettingsOpen(true)}
                className="w-full bg-[#1A1A22]/15 hover:bg-[#1A1A22]/25 text-[#1A1A22] border border-[#1A1A22]/20 rounded-lg h-8 text-xs font-semibold shadow-none transition"
              >
                <UserCog className="w-3.5 h-3.5 mr-1.5" />
                Profile & Settings
              </Button>
              <Button
                type="button"
                onClick={() => setIsPasswordResetOpen(true)}
                className="w-full bg-[#1A1A22]/15 hover:bg-[#1A1A22]/25 text-[#1A1A22] border border-[#1A1A22]/20 rounded-lg h-8 text-xs font-semibold shadow-none transition"
              >
                <KeyRound className="w-3.5 h-3.5 mr-1.5" />
                Reset Password (OTP)
              </Button>
              <Button
                type="button"
                onClick={handleLogout}
                className="w-full bg-[#1A1A22] hover:bg-black text-white rounded-lg h-8 text-xs font-semibold transition"
              >
                <LogOut className="w-3.5 h-3.5 mr-1.5" />
                Sign out
              </Button>
            </div>
          </div>
        </div>
      </aside>

      <div className="flex-1 flex flex-col overflow-hidden bg-[#16161C] rounded-2xl border border-white/5">
        <header className="px-8 py-5 flex items-center justify-between border-b border-white/5">
          <div>
            <div className="text-[11px] uppercase tracking-wider text-white/40">Overview</div>
            <h2 className="text-white mt-0.5">{activeLabel}</h2>
          </div>
          <div className="flex items-center gap-3">
            <NotificationCenter />
            <button
              type="button"
              onClick={() => setIsProfileSettingsOpen(true)}
              title="Click to customize profile and settings"
              className="flex items-center gap-2 rounded-full border border-white/10 bg-[#1D1D25] py-1 pl-1 pr-3 hover:border-yellow-400/40 transition group cursor-pointer"
            >
              <div className="w-7 h-7 rounded-full overflow-hidden bg-gradient-to-br from-[#E5202A] to-[#FFD60A] flex items-center justify-center text-xs font-bold text-white shadow-sm shrink-0">
                {user?.avatar_url ? (
                  <img src={user.avatar_url} alt={user.name} className="w-full h-full object-cover" />
                ) : (
                  (user?.name || 'I').charAt(0).toUpperCase()
                )}
              </div>
              <span className="text-xs font-medium text-white/80 group-hover:text-yellow-300 transition max-w-[100px] truncate">
                {user?.name?.split(' ')[0] || user?.username || 'Inventory'}
              </span>
            </button>
          </div>
        </header>
        <main className="flex-1 overflow-y-auto scrollbar-hide p-8 bg-[#0E0E12]">
          {renderContent()}
        </main>
      </div>

      <PortalPasswordResetModal
        isOpen={isPasswordResetOpen}
        onClose={() => setIsPasswordResetOpen(false)}
      />
      <PortalProfileSettingsModal
        isOpen={isProfileSettingsOpen}
        onClose={() => setIsProfileSettingsOpen(false)}
      />
    </div>
  );
}
