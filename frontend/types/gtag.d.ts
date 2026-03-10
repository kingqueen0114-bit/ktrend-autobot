interface GtagEventParams {
  [key: string]: string | number | boolean
}

interface Window {
  gtag?: (
    command: 'event' | 'config' | 'set',
    targetOrName: string,
    params?: GtagEventParams
  ) => void
}
