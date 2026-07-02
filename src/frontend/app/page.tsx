import Link from 'next/link';
import { ArrowRight, Languages, Mic, Type, Wand2 } from 'lucide-react';

export default function HomePage() {
  return (
    <main className="container flex min-h-screen flex-col items-center justify-center gap-12 py-20">
      <div className="flex flex-col items-center gap-4 text-center">
        <div className="rounded-full bg-primary/10 px-4 py-1.5 text-sm font-medium text-primary">
          Video Localization AI Studio
        </div>
        <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">
          Bản địa hóa video <br />
          <span className="text-primary">tự động với AI</span>
        </h1>
        <p className="max-w-2xl text-lg text-muted-foreground">
          Tự động dịch và lồng tiếng video sang tiếng Việt. Từ upload đến xuất
          YouTube, tất cả trong một nơi.
        </p>
        <Link
          href="/dashboard"
          className="inline-flex items-center gap-2 rounded-lg bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground shadow transition hover:bg-primary/90"
        >
          Bắt đầu
          <ArrowRight className="h-4 w-4" />
        </Link>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <FeatureCard
          icon={<Mic className="h-6 w-6" />}
          title="Speech-to-Text"
          description="Whisper AI nhận diện giọng nói đa ngôn ngữ với timestamp chính xác"
        />
        <FeatureCard
          icon={<Languages className="h-6 w-6" />}
          title="AI Translation"
          description="Dịch tự nhiên sang tiếng Việt, giữ tên riêng và thuật ngữ kỹ thuật"
        />
        <FeatureCard
          icon={<Type className="h-6 w-6" />}
          title="Voice Dubbing"
          description="Nhiều giọng đọc tiếng Việt tự nhiên, đồng bộ với video gốc"
        />
        <FeatureCard
          icon={<Wand2 className="h-6 w-6" />}
          title="Branding & Export"
          description="Subtitle, intro/outro, watermark, xuất MP4/2K/4K chất lượng cao"
        />
      </div>
    </main>
  );
}

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="rounded-xl border bg-card p-6 text-card-foreground shadow-sm transition hover:shadow-md">
      <div className="mb-3 inline-flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
        {icon}
      </div>
      <h3 className="mb-1 font-semibold">{title}</h3>
      <p className="text-sm text-muted-foreground">{description}</p>
    </div>
  );
}
