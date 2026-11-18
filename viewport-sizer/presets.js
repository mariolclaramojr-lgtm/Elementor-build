// Built-in presets. Height omitted = keep the current height.
// dpr / mobile are only used in Emulate mode.
const PRESET_GROUPS = [
  {
    name: 'Phones',
    items: [
      { label: 'iPhone SE', width: 375, height: 667, dpr: 2, mobile: true },
      { label: 'iPhone 15', width: 393, height: 852, dpr: 3, mobile: true },
      { label: 'iPhone 15 Pro Max', width: 430, height: 932, dpr: 3, mobile: true },
      { label: 'Pixel 8', width: 412, height: 915, dpr: 2.625, mobile: true },
      { label: 'Galaxy S24', width: 360, height: 780, dpr: 3, mobile: true },
    ],
  },
  {
    name: 'Tablets',
    items: [
      { label: 'iPad Mini', width: 768, height: 1024, dpr: 2, mobile: true },
      { label: 'iPad Air', width: 820, height: 1180, dpr: 2, mobile: true },
      { label: 'iPad Pro 12.9"', width: 1024, height: 1366, dpr: 2, mobile: true },
    ],
  },
  {
    name: 'Desktop',
    items: [
      { label: '1280 × 800', width: 1280, height: 800 },
      { label: '1366 × 768', width: 1366, height: 768 },
      { label: '1440 × 900', width: 1440, height: 900 },
      { label: '1536 × 864', width: 1536, height: 864 },
      { label: '1920 × 1080', width: 1920, height: 1080 },
      { label: '2560 × 1440', width: 2560, height: 1440 },
    ],
  },
  {
    // Elementor's default breakpoints, each side of the edge.
    name: 'Elementor breakpoints',
    items: [
      { label: 'Mobile 767', width: 767 },
      { label: 'Mobile Extra 880', width: 880 },
      { label: 'Tablet 1024', width: 1024 },
      { label: 'Tablet Extra 1200', width: 1200 },
      { label: 'Laptop 1366', width: 1366 },
      { label: 'Desktop 1367', width: 1367 },
      { label: 'Widescreen 2400', width: 2400 },
    ],
  },
];
