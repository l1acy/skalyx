import { lazy } from "react";
import Header from "./components/header"
import { useTranslation } from "./i18n/context";

const DashboardGrid = lazy(() => import('./features/dashboard/components/DashboardGrid'));

export function App() {
  const { t} = useTranslation();

  return (
    <div>
      <Header />
      <h1 className="px-6 text-2xl font-semibold italic">
        {t('wip')}
      </h1>
      <DashboardGrid/>
    </div>
  )
}

export default App
