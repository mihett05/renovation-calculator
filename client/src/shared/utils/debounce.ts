import { useCallback } from 'react';

export function debounce<T extends (...args: Parameters<T>) => ReturnType<T>>(
  callback: T,
  timeout: number,
) {
  let timeoutId: number | null = null;
  return (...args: Parameters<T>) => {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    timeoutId = setTimeout(() => {
      callback(...args);
    }, timeout) as unknown as number;
  };
}

export function useDebounce<
  T extends (...args: Parameters<T>) => ReturnType<T>,
>(callback: T, timeout: number) {
  return useCallback(debounce(callback, timeout), []);
}
