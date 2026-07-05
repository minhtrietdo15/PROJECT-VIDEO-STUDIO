import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Timeline, type SubtitleSegment } from '@/components/subtitle/timeline';

const mockSegments: SubtitleSegment[] = [
  { id: '1', start: 0, end: 5, text: 'Hello world' },
  { id: '2', start: 5, end: 10, text: 'This is a test' },
];

describe('Timeline', () => {
  it('renders timeline with segments', () => {
    render(<Timeline duration={300} segments={mockSegments} />);
    expect(screen.getByText('Hello world')).toBeInTheDocument();
    expect(screen.getByText('This is a test')).toBeInTheDocument();
  });

  it('calls onSegmentSelect when segment is clicked', () => {
    const mockSelect = vi.fn();
    render(
      <Timeline
        duration={300}
        segments={mockSegments}
        onSegmentSelect={mockSelect}
      />
    );
    
    const segment = screen.getByText('Hello world').closest('.cursor-pointer');
    fireEvent.click(segment!);
    
    expect(mockSelect).toHaveBeenCalledWith('1');
  });

  it('displays time format correctly', () => {
    render(<Timeline duration={65} segments={mockSegments} />);
    expect(screen.getByText('0:00')).toBeInTheDocument();
    expect(screen.getByText('0:05')).toBeInTheDocument();
  });
});