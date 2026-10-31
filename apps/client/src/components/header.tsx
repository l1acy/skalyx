import {
  Clock,
  Monitor,
  Moon,
  Save,
  Settings,
  Sun,
  Wrench,
  type IconNode,
} from "lucide"
import { Button } from "./ui/button"
import { useState } from "react"
import { MorphIcon } from "morphicons/react"
import { useTheme, type Theme } from "./theme-provider"
import { LogoHouseToggle } from "./logo-toggler"
import { useTranslation } from "@/i18n/context"
import { LanguageCombobox } from "./language-combobox"

const ThemeIcons: Record<Theme, IconNode> = {
  dark: Moon,
  light: Sun,
  system: Monitor,
}

function HeaderItem({
  label,
  iconDefault,
  iconHover,
}: {
  label: string
  iconDefault: IconNode
  iconHover: IconNode
}) {
  const [isFocused, setIsFocused] = useState(false)

  return (
    <Button
      variant={"ghost"}
      onMouseEnter={() => setIsFocused(true)}
      onMouseLeave={() => setIsFocused(false)}
    >
      <MorphIcon icon={isFocused ? iconHover : iconDefault} />

      {label}
    </Button>
  )
}

function Logo() {
  const [isFocused, setIsFocused] = useState(false)

  return (
    <Button
      variant={"ghost"}
      className="flex flex-row items-center gap-1.5 px-3"
      onMouseEnter={() => setIsFocused(true)}
      onMouseLeave={() => setIsFocused(false)}
    >
      <LogoHouseToggle isToggled={isFocused} />

      <p className="font-semibold">Skalyx</p>
    </Button>
  )
}

export default function Header() {
  const { theme, setTheme } = useTheme()
  const { t } = useTranslation()

  return (
    <header className="flex flex-row px-4 py-4">
      <Logo />
      <HeaderItem
        label={t("historyTab")}
        iconDefault={Clock}
        iconHover={Save}
      />
      <HeaderItem
        label={t("settingsTab")}
        iconDefault={Settings}
        iconHover={Wrench}
      />

      <div className="flex-1"></div>

      <LanguageCombobox/>
      <Button
        size={"icon"}
        onClick={() => setTheme(theme == "dark" ? "light" : "dark")}
        variant={"outline"}
      >
        <MorphIcon icon={ThemeIcons[theme]} />
      </Button>
    </header>
  )
}
