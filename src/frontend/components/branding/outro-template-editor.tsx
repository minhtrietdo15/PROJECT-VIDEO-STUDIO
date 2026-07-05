'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ThumbsUp, Bell, QrCode, Globe, Youtube, Facebook, Instagram, Twitter } from 'lucide-react';

export interface OutroTemplate {
  subscribeAnimation: boolean;
  likeAnimation: boolean;
  qrCodeUrl?: string;
  websiteUrl?: string;
  socialLinks: {
    youtube?: string;
    facebook?: string;
    tiktok?: string;
    instagram?: string;
  };
}

export interface OutroTemplateEditorProps {
  template: OutroTemplate;
  onTemplateChange?: (template: OutroTemplate) => void;
  onSave?: () => void;
  className?: string;
}

export function OutroTemplateEditor({
  template,
  onTemplateChange,
  onSave,
  className,
}: OutroTemplateEditorProps) {
  const updateTemplate = (updates: Partial<OutroTemplate>) => {
    onTemplateChange?.({ ...template, ...updates });
  };

  const updateSocialLink = (platform: keyof OutroTemplate['socialLinks'], value: string) => {
    onTemplateChange?.({
      ...template,
      socialLinks: { ...template.socialLinks, [platform]: value },
    });
  };

  return (
    <div className={cn('space-y-4', className)}>
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Subscribe & Like</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center gap-2">
            <input
              id="subscribe-anim"
              type="checkbox"
              checked={template.subscribeAnimation}
              onChange={(e) => updateTemplate({ subscribeAnimation: e.target.checked })}
              className="h-4 w-4"
            />
            <Label htmlFor="subscribe-anim" className="flex items-center gap-2">
              <Bell className="h-4 w-4" /> Subscribe Button Animation
            </Label>
          </div>
          <div className="flex items-center gap-2">
            <input
              id="like-anim"
              type="checkbox"
              checked={template.likeAnimation}
              onChange={(e) => updateTemplate({ likeAnimation: e.target.checked })}
              className="h-4 w-4"
            />
            <Label htmlFor="like-anim" className="flex items-center gap-2">
              <ThumbsUp className="h-4 w-4" /> Like Animation
            </Label>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">QR Code</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-2">
            <QrCode className="h-4 w-4 text-muted-foreground" />
            <Input
              value={template.qrCodeUrl || ''}
              onChange={(e) => updateTemplate({ qrCodeUrl: e.target.value })}
              placeholder="Enter URL for QR code..."
            />
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Website</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-2">
            <Globe className="h-4 w-4 text-muted-foreground" />
            <Input
              value={template.websiteUrl || ''}
              onChange={(e) => updateTemplate({ websiteUrl: e.target.value })}
              placeholder="https://your-website.com"
            />
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Social Links</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center gap-2">
            <Youtube className="h-4 w-4 text-red-500" />
            <Input
              value={template.socialLinks.youtube || ''}
              onChange={(e) => updateSocialLink('youtube', e.target.value)}
              placeholder="YouTube channel URL"
            />
          </div>
          <div className="flex items-center gap-2">
            <Facebook className="h-4 w-4 text-blue-600" />
            <Input
              value={template.socialLinks.facebook || ''}
              onChange={(e) => updateSocialLink('facebook', e.target.value)}
              placeholder="Facebook page URL"
            />
          </div>
          <div className="flex items-center gap-2">
            <Instagram className="h-4 w-4 text-pink-500" />
            <Input
              value={template.socialLinks.instagram || ''}
              onChange={(e) => updateSocialLink('instagram', e.target.value)}
              placeholder="Instagram URL"
            />
          </div>
          <div className="flex items-center gap-2">
            <Twitter className="h-4 w-4 text-blue-400" />
            <Input
              value={template.socialLinks.tiktok || ''}
              onChange={(e) => updateSocialLink('tiktok', e.target.value)}
              placeholder="TikTok URL"
            />
          </div>
        </CardContent>
      </Card>

      <Button className="w-full" onClick={onSave}>
        Save as Template
      </Button>
    </div>
  );
}