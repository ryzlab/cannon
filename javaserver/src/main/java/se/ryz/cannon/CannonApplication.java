package se.ryz.cannon;

import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import javax.usb.*;

@SpringBootApplication
public class CannonApplication implements ApplicationRunner {

	public static void main(String[] args) {
		SpringApplication.run(CannonApplication.class, args);
	}

	@Override
	public void run( ApplicationArguments args ) throws Exception
	{
		MissileLauncher ml = new MissileLauncher();
		// Search for the missile launcher USB device and stop when not found
		UsbDevice device = ml.findMissileLauncher(
				UsbHostManager.getUsbServices().getRootUsbHub());
		if (device == null)
		{
			System.err.println("Missile launcher not found.");
			System.exit(1);
			return;
		}

		// Claim the interface
		UsbConfiguration configuration = device.getUsbConfiguration((byte) 1);
		UsbInterface iface = configuration.getUsbInterface((byte) 0);
		iface.claim(new UsbInterfacePolicy()
		{
			@Override
			public boolean forceClaim(UsbInterface usbInterface)
			{
				return true;
			}
		});

		// Read commands and execute them
		System.out.println("WADX = Move, S = Stop, F = Fire, Q = Exit");
		boolean exit = false;
		while (!exit)
		{
			System.out.print("> ");
			char key = ml.readKey();
			switch (key)
			{
				case 'w':
					ml.sendCommand(device, MissileLauncher.CMD_UP);
					break;

				case 'x':
					ml.sendCommand(device, MissileLauncher.CMD_DOWN);
					break;

				case 'a':
					ml.sendCommand(device, MissileLauncher.CMD_LEFT);
					break;

				case 'd':
					ml.sendCommand(device, MissileLauncher.CMD_RIGHT);
					break;

				case 'f':
					ml.sendCommand(device, MissileLauncher.CMD_FIRE);
					break;

				case 's':
					ml.sendCommand(device, 0);
					break;

				case 'q':
					exit = true;
					break;

				default:
			}
		}
		System.out.println("Exiting");



		System.out.println( "Name: ");
	}
}
