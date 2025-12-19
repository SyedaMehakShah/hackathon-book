import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import { useLocation } from '@docusaurus/router';
import { ThemeClassNames } from '@docusaurus/theme-common';
import { useBlogMetadata } from '@docusaurus/plugin-content-blog/client';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

// This component only renders on smaller screens
function DocSidebarMobileSecondaryMenu({ sidebar, path }) {
  const location = useLocation();
  
  // Find the current category or item based on the path
  const findCurrentCategory = (items) => {
    for (const item of items) {
      if (item.type === 'category') {
        if (item.items.some(subItem => subItem.href === location.pathname)) {
          return item;
        }
        const nestedResult = findCurrentCategory(item.items);
        if (nestedResult) return nestedResult;
      } else if (item.href === location.pathname) {
        return item;
      }
    }
    return null;
  };

  const currentCategory = findCurrentCategory(sidebar);
  
  return (
    <div className="menu__list">
      {sidebar.map((item, idx) => (
        <div key={idx} className="menu__list-item">
          <div
            className={clsx('menu__button', {
              'menu__button--active': currentCategory?.label === item.label,
            })}
          >
            {item.label}
          </div>
          {currentCategory?.label === item.label && item.type === 'category' && (
            <ul className="menu__list">
              {item.items.map((subItem, subIdx) => (
                <li key={subIdx} className="menu__list-item">
                  <a
                    href={subItem.href}
                    className={clsx('menu__link', {
                      'menu__link--active': location.pathname === subItem.href,
                    })}
                  >
                    {subItem.label}
                  </a>
                </li>
              ))}
            </ul>
          )}
        </div>
      ))}
    </div>
  );
}

// Main mobile sidebar component
function DocSidebarMobile(props) {
  const { sidebar, onClose, isHidden } = props;
  const location = useLocation();
  const [shown, setShown] = useState(false);

  useEffect(() => {
    if (!isHidden) {
      setShown(true);
      return () => setShown(false);
    }
    return () => {};
  }, [isHidden]);

  if (!shown) {
    return null;
  }

  return (
    <div
      className={clsx(
        'doc-sidebar-mobile',
        'position-fixed',
        'top-0',
        'bottom-0',
        'left-0',
        'z-index-1020',
        'pt-4',
        'd-lg-none',
        'd-flex',
        'flex-column',
        'bg-white',
        'min-h-100vh',
        'border-end',
        'border-md',
        'shadow',
        {
          'd-none': isHidden,
          'opacity-0': isHidden,
          'transition-opacity': !isHidden,
        }
      )}
      style={{
        width: 300,
        transform: isHidden ? 'translateX(-100%)' : 'translateX(0)',
        transition: 'transform 0.3s ease',
      }}
    >
      <div className="flex-grow-1 overflow-auto">
        <div className="position-sticky top-0 bg-white border-bottom py-2 px-3">
          <button
            type="button"
            className="btn-close"
            aria-label="Close"
            onClick={onClose}
            style={{ position: 'absolute', right: 10, top: 10 }}
          />
          <h3 className="h6 mb-0">Table of Contents</h3>
        </div>
        <nav
          className={clsx(ThemeClassNames.docs.docSidebarMenu, 'px-2')}
          aria-label="Sidebar navigation"
        >
          <DocSidebarMobileSecondaryMenu
            sidebar={sidebar}
            path={location.pathname}
          />
        </nav>
      </div>
    </div>
  );
}

export default DocSidebarMobile;