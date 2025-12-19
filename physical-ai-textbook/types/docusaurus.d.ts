// Type declaration for Docusaurus modules that may not have proper TypeScript support

declare module '@docusaurus/useDocusaurusContext' {
  import { DocusaurusContext } from '@docusaurus/types';
  const useDocusaurusContext: () => DocusaurusContext;
  export default useDocusaurusContext;
}

declare module '@docusaurus/core' {
  import { DocusaurusContext } from '@docusaurus/types';
  export function useDocusaurusContext(): DocusaurusContext;
}