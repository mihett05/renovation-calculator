import { Card, Image, Text, Button, Group, Badge } from '@mantine/core';
import type { Wall, WallType } from '~/shared/api/api';

type WallCardProps = {
  wall: Wall;
};

const TYPES: Record<WallType, [string, string]> = {
  wallpaper: ['Обои', 'pink'],
  ceramic: ['Керамика', 'gray'],
  paint: ['Краска', 'brown'],
};

export function WallCard({ wall }: WallCardProps) {
  return (
    <Card shadow="sm" padding="lg" radius="md" withBorder>
      <Card.Section>
        <Image src={wall.photo} height={160} alt="Фото" />
      </Card.Section>

      <Group justify="space-between" mt="md" mb="xs">
        <Text fz="sm">{wall.name}</Text>
        <Badge color={TYPES[wall.wallType][1]}>{TYPES[wall.wallType][0]}</Badge>
        <Badge color="blue">{Math.ceil(wall.price)} ₽/м2</Badge>
      </Group>

      <Text size="sm" c="dimmed">
        Цвет: {wall.color}
      </Text>

      <Group>
        <Button
          color="blue"
          fullWidth
          mt="md"
          radius="md"
          component="a"
          href={wall.url}
          target="_blank"
        >
          Купить
        </Button>
      </Group>
    </Card>
  );
}
