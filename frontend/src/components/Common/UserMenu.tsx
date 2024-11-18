import React, { useEffect, useState } from 'react';
import {
  Box,
  IconButton,
  Menu,
  MenuButton,
  MenuItem,
  MenuList,
  Badge, 
  HStack
} from "@chakra-ui/react"
import { Link } from "@tanstack/react-router"
import { FaUserAstronaut } from "react-icons/fa"
import { FiLogOut, FiUser, FiMessageCircle } from "react-icons/fi"

import useAuth from "../../hooks/useAuth"

const UserMenu = () => {
  const [messageCount, setMessageCount] = useState(0);

  // useEffect(() => {
  //   // Replace with your API call to fetch the message count
  //   async function fetchMessageCount() {
  //     const response = await fetch('/api/messages/count');
  //     const data = await response.json();
  //     setMessageCount(data.count); // Assuming the count is in `data.count`
  //   }

  //   fetchMessageCount();
  // }, []);

  const { logout } = useAuth()

  const handleLogout = async () => {
    logout()
  }

  return (
    <>
      {/* Desktop */}
      <Box
        display={{ base: "none", md: "block" }}
        position="fixed"
        top={4}
        right={4}
      >
        <Menu>
          <MenuButton
            as={IconButton}
            aria-label="Options"
            icon={<FaUserAstronaut color="white" fontSize="18px" />}
            bg="ui.main"
            isRound
            data-testid="user-menu"
          />
          <MenuList>
            <MenuItem icon={<FiUser fontSize="18px" />} as={Link} to="settings">
              My profile
            </MenuItem>
            <MenuItem icon={<FiMessageCircle fontSize="18px" />} as={Link} to="messages">
             <HStack justifyContent="space-between" w="100%">
                <span>Messages</span>
                {messageCount > 0 && (
                  <Badge colorScheme="green" fontSize="sm">
                    {messageCount}
                  </Badge>
                )}
              </HStack>
            </MenuItem>
            <MenuItem
              icon={<FiLogOut fontSize="18px" />}
              onClick={handleLogout}
              color="ui.danger"
              fontWeight="bold"
            >
              Log out
            </MenuItem>
          </MenuList>
        </Menu>
      </Box>
    </>
  )
}

export default UserMenu
