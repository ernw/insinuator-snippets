import java.io.*;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.LinkedList;
import java.util.List;

public class FirmwareFile {
    private final List<byte[]> frames = new LinkedList();

    public FirmwareFile(InputStream stream) throws IOException {
        this.parse(stream);
    }

    public List<byte[]> getFrames() {
        return this.frames;
    }

    private void parse(InputStream stream) throws IOException {
        try {
            this.readFrames(stream);
        } catch (IOException var3) {
        }
    }

    private void readFrames(InputStream stream) throws IOException {
        this.frames.clear();

        for(byte[] frame = this.readFrame(stream); frame != null; frame = this.readFrame(stream)) {
            this.frames.add(frame);
        }

    }

    private byte[] readFrame(InputStream stream) throws IOException {
        int length = this.readLength(stream);
        return length > 0?this.readFrameData(stream, length):null;
    }

    private int readLength(InputStream stream) throws IOException {
        int high = this.readByte(stream);
        int low = this.readByte(stream);
        return high << 8 | low;
    }

    private byte[] readFrameData(InputStream stream, int length) throws IOException {
        ByteArrayOutputStream outStream = new ByteArrayOutputStream();

        for(int result = 0; result < length; ++result) {
            int value = this.readByte(stream);
            outStream.write(value);
        }

        byte[] var6 = outStream.toByteArray();
        outStream.close();
        return var6;
    }

    private int readByte(InputStream stream) throws IOException {
        int high = stream.read();
        int low = stream.read();
        return this.createByte(high, low);
    }

    private int createByte(int high, int low) {
        return this.fromHex(high) << 4 | this.fromHex(low);
    }

    private int fromHex(int value) {
        return 48 <= value && value <= 57?value - 48:(97 <= value && value <= 102?value - 97 + 10:(65 <= value && value <= 70?value - 65 + 10:0));
    }
}
