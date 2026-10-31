import {
  createContext,
  useContext,
  useState,
  useCallback,
  useMemo,
  type ReactNode,
} from 'react';
import en from './locales/en';
import ru from './locales/ru';

const dictionaries = { en, ru } as const;

export type Lang = keyof typeof dictionaries;
type Dictionary = typeof en;

type PathImpl<T, K extends keyof T> = K extends string
  ? T[K] extends (...args: any[]) => any
    ? K
    : T[K] extends Record<string, unknown>
    ? `${K}.${PathImpl<T[K], keyof T[K]>}`
    : K
  : never;

type TranslationKey = PathImpl<Dictionary, keyof Dictionary>;

type ValueAtPath<T, P extends string> = P extends `${infer Head}.${infer Rest}`
  ? Head extends keyof T
    ? ValueAtPath<T[Head], Rest>
    : never
  : P extends keyof T
  ? T[P]
  : never;

function getNested(obj: Record<string, unknown>, path: string): unknown {
  return path.split('.').reduce<unknown>((acc, key) => {
    if (acc && typeof acc === 'object') return (acc as Record<string, unknown>)[key];
    return undefined;
  }, obj);
}

interface I18nContextValue {
  lang: Lang;
  changeLanguage: (lang: Lang) => void;
  t: <K extends TranslationKey>(
    key: K,
    ...args: ValueAtPath<Dictionary, K> extends (...a: infer A) => any ? A : []
  ) => string;
}

const I18nContext = createContext<I18nContextValue | null>(null);

interface I18nProviderProps {
  children: ReactNode;
  defaultLang?: Lang;
}

function isValidLang(value: string): value is Lang {
  return value in dictionaries;
}

export function I18nProvider({ children, defaultLang = 'en' }: I18nProviderProps) {
  const [lang, setLang] = useState<Lang>(() => {
    const stored = localStorage.getItem('lang');
    if (stored && isValidLang(stored)) return stored;

    const browserLang = navigator.language.slice(0, 2);
    if (isValidLang(browserLang)) return browserLang;

    return defaultLang;
  });

  const changeLanguage = useCallback((newLang: Lang) => {
    setLang(newLang);
    localStorage.setItem('lang', newLang);
  }, []);

  const t = useCallback<I18nContextValue['t']>(
    (key, ...args) => {
      const dict = dictionaries[lang] ?? dictionaries[defaultLang];
      const value = getNested(dict, key);

      if (typeof value === 'function') return value(...args);
      if (typeof value === 'string') return value;
      return key;
    },
    [lang, defaultLang]
  );

  const value = useMemo<I18nContextValue>(
    () => ({ lang, changeLanguage, t }),
    [lang, changeLanguage, t]
  );

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

export function useTranslation(): I18nContextValue {
  const ctx = useContext(I18nContext);
  if (!ctx) throw new Error('useTranslation must be used within I18nProvider');
  return ctx;
}