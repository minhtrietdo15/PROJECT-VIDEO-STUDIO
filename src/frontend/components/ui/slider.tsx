import * as React from 'react';
import { cn } from '@/lib/utils';

export interface SliderProps
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'value' | 'onChange'> {
  value?: number[];
  onValueChange?: (value: number[]) => void;
}

const Slider = React.forwardRef<HTMLInputElement, SliderProps>(
  ({ className, value = [0], onValueChange, ...props }, ref) => {
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      onValueChange?.([parseFloat(e.target.value)]);
    };

    return (
      <input
        type="range"
        ref={ref}
        className={cn(
          'w-full cursor-pointer appearance-none rounded-lg bg-muted focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
          className
        )}
        value={value[0]}
        onChange={handleChange}
        {...props}
      />
    );
  }
);
Slider.displayName = 'Slider';

export { Slider };
