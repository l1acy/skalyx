import Header from "./components/header"
import { useTranslation } from "./i18n/context";

export function App() {
  const { t} = useTranslation();

  return (
    <div>
      <Header />
      <h1 className="px-6 text-2xl font-semibold italic">
        {t('wip')}
      </h1>

    </div>
  )
}

export default App
