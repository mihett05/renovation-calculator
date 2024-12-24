import {
  Box,
  Button,
  Group,
  List,
  Mark,
  NumberInput,
  Stack,
  Title,
  useMantineTheme,
} from '@mantine/core';
import { useState } from 'react';
import SearchFloors from '~/features/search-floors';
import SearchWalls from '~/features/search-walls';
import type { Floor, Wall } from '~/shared/api/api';

function Calculator() {
  const theme = useMantineTheme();

  const [wallHeight, setWallHeight] = useState<number | null>(2);

  const [floorWidth, setFloorWidth] = useState<number | null>(10);
  const [floorHeight, setFloorHeight] = useState<number | null>(10);

  const [wall, setWall] = useState<Wall | null>(null);
  const [floor, setFloor] = useState<Floor | null>(null);

  const wallPrice =
    floorWidth && floorHeight && wallHeight && wall
      ? wall.price * wallHeight * floorHeight * 2 +
        wall.price * wallHeight * floorWidth * 2
      : null;
  const floorPrice =
    floorWidth && floorHeight && floor
      ? floorWidth * floorHeight * floor.price
      : null;

  const MAX_WIDTH = 400;
  const MAX_HEIGHT = 400;

  const width = (floorWidth || 10) * 20;
  const height = (floorHeight || 10) * 20;

  const scale = Math.min(MAX_WIDTH / width, MAX_HEIGHT / height);

  return (
    <Group gap={150} align="start">
      <Stack>
        <Title>Расчёт стоимости</Title>
        <NumberInput
          label="Высота комнаты"
          value={wallHeight ?? undefined}
          onValueChange={(value) => setWallHeight(value.floatValue || null)}
        />
        <SearchWalls selected={wall} onSelected={setWall} />
        <SearchFloors selected={floor} onSelected={setFloor} />
        <List>
          {wallPrice && (
            <List.Item>
              Настенное покрытие: <Mark>{wallPrice.toFixed(2)}₽</Mark>
            </List.Item>
          )}
        </List>
        <List>
          {floorPrice && (
            <List.Item>
              Напольное покрытие: <Mark>{floorPrice.toFixed(2)}₽</Mark>
            </List.Item>
          )}
        </List>
        <List>
          {wallPrice && floorPrice && (
            <List.Item
              style={{
                fontWeight: 'bold',
              }}
            >
              Итого: <Mark>{(wallPrice + floorPrice).toFixed(2)}₽</Mark>
            </List.Item>
          )}
        </List>
        <Group>
          <Button
            disabled={wall === null}
            component="a"
            href={wall?.url}
            target="_blank"
          >
            Купить настенное покрытие
          </Button>
          <Button
            bg="teal"
            disabled={floor === null}
            component="a"
            href={floor?.url}
            target="_blank"
          >
            Купить напольное покрытие
          </Button>
        </Group>
      </Stack>

      <Box>
        <Title>Схема комнаты</Title>
        <Stack
          style={{
            padding: '10em',
            border: `1px solid ${theme.colors.gray[4]}`,
          }}
          align="center"
        >
          <Group align="center">
            <NumberInput
              label="Ширина пола"
              value={floorWidth ?? undefined}
              onValueChange={(e) => setFloorWidth(e.floatValue || null)}
            />
            <NumberInput
              label="Длина пола"
              value={floorHeight ?? undefined}
              onValueChange={(e) => setFloorHeight(e.floatValue || null)}
            />
          </Group>
          <Box
            style={{
              width: width * scale,
              maxWidth: MAX_WIDTH,
              height: height * scale,
              maxHeight: MAX_HEIGHT,
              border: '4px solid black',
            }}
          />
        </Stack>
      </Box>
    </Group>
  );
}

export default Calculator;
