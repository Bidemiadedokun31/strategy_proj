export class Logger {
  constructor(private context: string) {}

  info(message: string, meta?: Record<string, any>): void {
    console.log(JSON.stringify({
      level: 'INFO',
      context: this.context,
      message,
      timestamp: new Date().toISOString(),
      ...meta,
    }));
  }

  error(message: string, meta?: Record<string, any>): void {
    console.error(JSON.stringify({
      level: 'ERROR',
      context: this.context,
      message,
      timestamp: new Date().toISOString(),
      ...meta,
    }));
  }

  warn(message: string, meta?: Record<string, any>): void {
    console.warn(JSON.stringify({
      level: 'WARN',
      context: this.context,
      message,
      timestamp: new Date().toISOString(),
      ...meta,
    }));
  }

  debug(message: string, meta?: Record<string, any>): void {
    if (process.env.DEBUG === 'true') {
      console.log(JSON.stringify({
        level: 'DEBUG',
        context: this.context,
        message,
        timestamp: new Date().toISOString(),
        ...meta,
      }));
    }
  }
}
