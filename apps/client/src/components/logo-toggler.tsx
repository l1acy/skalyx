import Logo from "./logo";
import {HouseIcon} from 'lucide-react'
import './logo-toggler.css'


export function LogoHouseToggle({isToggled}: {isToggled: boolean}) {
  return (
    <button
      type="button"
      className="icon-swap"
    >
      <span className="icon-swap__stack">
        <span
          className={`icon-swap__icon ${isToggled ? "is-hidden" : "is-visible"}`}
        >
          <Logo />
        </span>
        <span
          className={`icon-swap__icon ${isToggled ? "is-visible" : "is-hidden"}`}
        >
          <HouseIcon />
        </span>
      </span>
    </button>
  );
}