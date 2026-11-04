import { Monitor, Moon, Sun, type IconNode } from "lucide";
import { MorphIcon } from "morphicons/react"
import { useState } from "react";
import { useTranslation, type TranslationKey } from "@/i18n/context";
import { Popover, PopoverContent, PopoverTrigger } from "./ui/popover";
import { cn } from "cn";
import { Icon } from "lucide-react";
import { buttonVariants } from "./ui/button";
import { useTheme, type Theme } from "./theme-provider";
import { Check } from "lucide-react"

const themes: { icon: IconNode, value: Theme, localizationKey: TranslationKey }[] = [
  {
    icon: Moon,
    value: 'dark',
    localizationKey: 'theme.dark'
  },
  {
    icon: Sun,
    value: 'light',
    localizationKey: 'theme.light'
  },
  {
    icon: Monitor,
    value: 'system',
    localizationKey: 'theme.system'
  },
] as const;

const ThemeIcons: Record<Theme, IconNode> = {
  dark: Moon,
  light: Sun,
  system: Monitor,
} as const;


export function ThemeSwitcher() {
  const [open, setOpen] = useState(false)
  const [value, setValue] = useState<string>()
  const { t } = useTranslation();
  const {theme, setTheme} = useTheme()

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger
        className={buttonVariants({ variant: "outline", size: "icon" })}
      >
        <MorphIcon icon={ThemeIcons[theme]}/>
      </PopoverTrigger>
      <PopoverContent className="w-55 p-0" align="start">
        <div className="max-h-55 overflow-y-auto p-1">
          {themes.length === 0 && (
            <p className="px-2 py-1.5 text-sm text-muted-foreground">
              {t('languageSelect.notFound')}
            </p>
          )}
          {themes.map(({ value: val, localizationKey, icon }) => (
            <button
              key={val}
              type="button"
              onClick={() => {
                setValue(val)
                setOpen(false)
                setTheme(val)
              }}
              className="flex w-full items-center gap-2 rounded-sm px-2 py-1.5 text-left text-sm hover:bg-accent"
            >
              <Check
                className={cn(
                  "h-4 w-4 shrink-0",
                  value === val ? "opacity-100" : "opacity-0"
                )}
              />
              <Icon iconNode={icon}/>
              {t(localizationKey)}
            </button>
          ))}
        </div>
      </PopoverContent>
    </Popover>
  )
}
