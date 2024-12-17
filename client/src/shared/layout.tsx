import { Link } from 'react-router';
import { Anchor, AppShell, Flex, NavLink } from '@mantine/core';
import { IconCalculator, IconCategory } from '@tabler/icons-react';

type LayoutProps = {
  children: React.ReactNode;
};

function Layout({ children }: LayoutProps) {
  return (
    <AppShell
      navbar={{
        width: 250,
        breakpoint: 'sm',
      }}
      padding="md"
    >
      <AppShell.Navbar>
        <NavLink
          component={Link}
          to="/"
          label="Калькулятор"
          leftSection={<IconCalculator size={32} />}
          styles={{
            label: {
              fontSize: '16pt',
            },
          }}
        />
        <NavLink
          component={Link}
          to="/catalog"
          label="Каталог"
          leftSection={<IconCategory size={32} />}
          styles={{
            label: {
              fontSize: '16pt',
            },
          }}
        />
      </AppShell.Navbar>
      <AppShell.Main>{children}</AppShell.Main>
    </AppShell>
  );
}

export default Layout;
