import {
  Clock,
  Save,
  Settings,
  Wrench,
  type IconNode,
} from "lucide"
import { Button } from "./ui/button"
import { useState } from "react"
import { MorphIcon } from "morphicons/react"
import { LogoHouseToggle } from "./logo-toggler"
import { useTranslation } from "@/i18n/context"
import { LanguageCombobox } from "./language-combobox"
import { ThemeSwitcher } from "./theme-switcher"

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

      <LanguageCombobox />
      <ThemeSwitcher/>
    </header>
  )
}
