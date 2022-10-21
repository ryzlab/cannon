package se.ryz.cannon.keyboardinput;

import javax.swing.*;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.util.HashMap;
import java.util.Map;

import static java.awt.event.KeyEvent.*;

public class KeyboardInput extends JFrame {

    public KeyboardInput() {
        setVisible(true);
        addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e) {
                System.exit(0);
            }
        });

        addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                KeyboardInput.this.keyPressed(e);
            }

            @Override
            public void keyReleased(KeyEvent e) {
                KeyboardInput.this.keyReleased(e);
            }
        });
    }

    Integer currentlyPressedKey = null;

    public void keyPressed(KeyEvent e) {
        if (currentlyPressedKey == null) {
            switch (e.getKeyCode()) {
                case VK_UP:
                    System.out.println("up");
                    break;
                case VK_DOWN:
                    System.out.println("down");
                    break;
                case VK_LEFT:
                    System.out.println("left");
                    break;
                case VK_RIGHT:
                    System.out.println("right");
                    break;
                case VK_SPACE:
                    System.out.println("fire");
                    break;
            }
            currentlyPressedKey = e.getKeyCode();
        }
    }
    public void keyReleased(KeyEvent e) {
        if (e.getKeyCode() == currentlyPressedKey) {
            if (e.getKeyCode() != VK_SPACE) {
                System.out.println("stop");
            }
            currentlyPressedKey = null;
        }
    }

    public static void main(String[] args) {
        new KeyboardInput();
    }
}
