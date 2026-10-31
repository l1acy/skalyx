import { StrictMode } from "react"
import { createRoot } from "react-dom/client"

import "./index.css"
import App from "./App.tsx"
import { ThemeProvider } from "@/components/theme-provider.tsx"
import ErrorBoundary from "./components/error-boundary.tsx"
import { PersistQueryClientProvider } from "@tanstack/react-query-persist-client"
import { idbPersister, queryClient } from "./queryClient.ts"
import { I18nProvider } from "./i18n/context.tsx"

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ErrorBoundary>
      <ThemeProvider>
        <I18nProvider>
          <PersistQueryClientProvider
            client={queryClient}
            persistOptions={{
              persister: idbPersister,
              maxAge: 24 * 60 * 60 * 1000,
              dehydrateOptions: {
                shouldDehydrateQuery: (query) =>
                  query.queryKey[0] === "weather",
              },
            }}
          >
            <App />
          </PersistQueryClientProvider>
        </I18nProvider>
      </ThemeProvider>
    </ErrorBoundary>
  </StrictMode>
)
