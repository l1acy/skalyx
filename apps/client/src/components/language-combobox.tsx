"use client"

import * as React from "react"
import { Check, LanguagesIcon } from "lucide-react"
import {  buttonVariants } from "@/components/ui/button"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { cn } from "@/lib/utils"
import { useTranslation, type Lang } from "@/i18n/context"

const languages: {value: Lang, label: string, iconPath: string}[] = [
  { value: "ru", label: "Русский", iconPath: '/flag-russia.svg' },
  { value: "en", label: "English", iconPath: '/flag-usa.svg' },
]

export function LanguageCombobox() {
  const [open, setOpen] = React.useState(false)
  const [value, setValue] = React.useState<string>()
  const { changeLanguage } = useTranslation();

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger
        className={buttonVariants({ variant: "outline", size: "icon" })}
      >
        <LanguagesIcon className="h-4 w-4" />
      </PopoverTrigger>
      <PopoverContent className="w-55 p-0" align="start">
        <div className="max-h-55 overflow-y-auto p-1">
          {languages.length === 0 && (
            <p className="px-2 py-1.5 text-sm text-muted-foreground">
              Языки не найдены
            </p>
          )}
          {languages.map(({ value: val, label, iconPath }) => (
            <button
              key={val}
              type="button"
              onClick={() => {
                setValue(val)
                setOpen(false)
                changeLanguage(val)
              }}
              className="flex w-full items-center gap-2 rounded-sm px-2 py-1.5 text-left text-sm hover:bg-accent"
            >
              <Check
                className={cn(
                  "h-4 w-4 shrink-0",
                  value === val ? "opacity-100" : "opacity-0"
                )}
              />
              <img src={iconPath} width={16} height={16}/>
              {label}
            </button>
          ))}
        </div>
      </PopoverContent>
    </Popover>
  )
}
