import java.io.*;
import java.util.List;
import java.nio.file.*;

public class FirmwareParser {
    public static void main(String[] args) throws IOException {
        if(args.length != 2){
            System.out.println("Need a source and a destination file path");
            System.exit(0);
        }

        InputStream stream = new FileInputStream(args[0]);
        FirmwareFile firmwareFile = new FirmwareFile(stream);
        List<byte[]> frames = firmwareFile.getFrames();
        Path path = Paths.get(args[1]);

        for(byte[] b: frames){
            Files.write(path, b, StandardOpenOption.CREATE, StandardOpenOption.APPEND);
        }

        System.out.println("Finished");
    }
}
