// Brand + form definitions. Single source of truth for the form page,
// server-side validation, the email, and the admin table.
//
// To change recipients, reps, or dropdown options: edit here and redeploy.

const SCHOOL_SITE_STATUS = [
  'Under Construction',
  'Under Renovation',
  'Occupied Existing School',
  'New School Opening',
];

const GENERAL_SITE_STATUS = [
  'Under Construction',
  'Under Renovation',
  'Occupied Existing Building',
  'New Building Opening',
];

const SALES_REPS = [
  'Terry (905) 475-7753',
  'Ryan (226) 747-5979',
  'Tiffany',
  'Shiva (416) 856-5080',
];

export const BRANDS = {
  schoolhouse: {
    slug: 'schoolhouse',
    name: 'Schoolhouse Products Ltd.',
    shortName: 'Schoolhouse',
    tagline: 'Furniture. All Kinds. Right Here.',
    accent: '#e8731a',
    reps: SALES_REPS,
    siteStatusOptions: SCHOOL_SITE_STATUS,
    mailTo: ['Sales@schoolhouseproducts.ca'],
    mailCc: ['Dinesh@schoolhouseproducts.ca'],
  },
  'office-central': {
    slug: 'office-central',
    name: 'Office Central',
    shortName: 'Office Central',
    tagline: 'Delivery Information',
    accent: '#1b3f7a',
    reps: SALES_REPS,
    siteStatusOptions: GENERAL_SITE_STATUS,
    mailTo: ['Sales@schoolhouseproducts.ca'],
    mailCc: ['Dinesh@schoolhouseproducts.ca'],
  },
  brant: {
    slug: 'brant',
    name: 'Brant Business Interiors',
    shortName: 'Brant',
    tagline: 'Delivery Information',
    accent: '#d4252a',
    reps: SALES_REPS,
    siteStatusOptions: GENERAL_SITE_STATUS,
    mailTo: ['Sales@schoolhouseproducts.ca'],
    mailCc: ['Dinesh@schoolhouseproducts.ca'],
  },
};

// Form fields in display order. `optionsFrom` pulls options off the brand.
// `allowOther` adds an "Other" choice with a free-text box.
export const FIELDS = [
  { key: 'rep', label: 'Sales Representative', type: 'select', required: true, optionsFrom: 'reps' },
  { key: 'quote', label: 'Quote #', type: 'text', required: true, placeholder: 'e.g. Q-10482' },
  { key: 'customer', label: 'Customer Name', type: 'text', required: true },
  { key: 'contactName', label: 'Contact Name (person receiving the delivery)', type: 'text', required: true },
  { key: 'contactEmail', label: 'Contact Email Address', type: 'email', required: true },
  { key: 'contactPhone', label: 'Contact Phone # (cell is best)', type: 'tel', required: true },
  {
    key: 'floor',
    label: 'What floor are the goods being taken to?',
    type: 'select',
    required: true,
    options: ['1st Floor', '2nd Floor', '3rd Floor'],
    allowOther: true,
  },
  {
    key: 'dock',
    label: 'Truck Level Loading Dock or Handbalm',
    type: 'select',
    required: false,
    options: ['Truck Level Loading Dock', 'Handbalm'],
  },
  {
    key: 'delivery',
    label: 'Installation or Straight Delivery',
    type: 'select',
    required: false,
    options: ['Installation', 'Straight Delivery'],
  },
  {
    key: 'timeRestriction',
    label: 'Delivery Time Restrictions',
    type: 'select',
    required: false,
    options: ['No Restrictions', '8:00 AM to 12 PM', '12 PM to 5 PM'],
    allowOther: true,
  },
  {
    key: 'access',
    label: 'Delivery Access',
    type: 'select',
    required: true,
    options: ['Stairs', 'Elevator', 'Elevator and Stairs', 'Main Floor'],
  },
  { key: 'siteStatus', label: 'Site Status', type: 'select', required: true, optionsFrom: 'siteStatusOptions' },
  { key: 'notes', label: 'Additional Information', type: 'textarea', required: false },
];

export const OTHER = 'Other';

export function getBrand(slug) {
  return Object.prototype.hasOwnProperty.call(BRANDS, slug) ? BRANDS[slug] : null;
}

// Options for a field, resolved against a brand.
export function fieldOptions(field, brand) {
  return field.optionsFrom ? brand[field.optionsFrom] : field.options || [];
}

// What the browser is allowed to see (no recipient addresses).
export function publicBrand(brand) {
  const { mailTo, mailCc, ...rest } = brand;
  return rest;
}

export function publicBrands() {
  return Object.values(BRANDS).map(publicBrand);
}

const MAX_LEN = { notes: 4000, default: 300 };

// Validates a raw body against FIELDS for a brand.
// Returns { values, errors } where values are cleaned strings.
export function validateSubmission(body, brand) {
  const values = {};
  const errors = {};
  for (const field of FIELDS) {
    let raw = body[field.key];
    raw = typeof raw === 'string' ? raw.trim() : '';
    const max = MAX_LEN[field.key] || MAX_LEN.default;
    if (raw.length > max) raw = raw.slice(0, max);

    if (field.type === 'select') {
      const options = fieldOptions(field, brand);
      if (raw === OTHER && field.allowOther) {
        let other = body[`${field.key}Other`];
        other = typeof other === 'string' ? other.trim().slice(0, MAX_LEN.default) : '';
        if (!other) {
          errors[field.key] = 'Please describe the "Other" choice.';
          continue;
        }
        raw = `Other: ${other}`;
      } else if (raw && !options.includes(raw)) {
        errors[field.key] = 'Please pick one of the choices.';
        continue;
      }
    }

    if (field.required && !raw) {
      errors[field.key] = 'This one is required.';
      continue;
    }
    if (field.type === 'email' && raw && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(raw)) {
      errors[field.key] = 'That email address does not look right.';
      continue;
    }
    values[field.key] = raw;
  }
  return { values, errors };
}
