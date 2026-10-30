import { Component, type ErrorInfo, type ReactNode } from "react"
import { CircleXIcon } from "lucide-react"
import { Button } from "./ui/button"

interface Props {
  children: ReactNode
  fallback?: (error: Error, reset: () => void) => ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export default class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    console.error("Render error:", error, info.componentStack)
  }

  handleReset = (): void => {
    this.setState({ hasError: false, error: null })
  }

  render(): ReactNode {
    const { hasError, error } = this.state

    if (hasError && error) {
      if (this.props.fallback) {
        return this.props.fallback(error, this.handleReset)
      }

      return (
        <div className="flex h-screen items-center justify-center">
          <div className="flex flex-col gap-2">
            <h1 className="flex gap-2 text-3xl font-semibold">
              <CircleXIcon size={36} />
              Произошла ошибка
            </h1>
            <p>Во время сборки страницы произошла ошибка</p>
            <div>
              <Button onClick={() => location.reload()}>Перезагрузить</Button>
              <Button onClick={this.handleReset} variant={"secondary"}>
                Попробовать снова
              </Button>
            </div>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
