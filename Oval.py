public class Oval
{
    // *** CREATE 5 PRIVATE INSTANCE VARIABLES FOR x1, y1, x2, y2, AND filled HERE ***
    private int x1;
    private int y1;
    private int x2;
    private int y2;
    private boolean filled;
    private static int numOvals = 0;


    // No-argument constructor
    public Oval()
    {
        x1 = 0;
        y1 = 0;
        x2 = 0;
        y2 = 0;
        filled = false;
        Oval.numOvals++;
    } 
    
    // Parameterized constructor with input values
    public Oval( int newX1, int newY1, int newX2, int newY2, boolean newFilled )
    {
        // *** COMPLETE THIS CODE ***
        this.setX1(newX1);
        this.setY1(newY1);
        this.setX2(newX2);
        this.setY2(newY2);
        this.filled = newFilled;
        Oval.numOvals++;
     }

     public int getX1(){
         return this.x1;
     }
     public int getY1(){
         return this.y1;
     }
     public int getX2(){
         return this.x2;
     }
     public int getY2(){
         return this.y2;
     }
     public boolean getFilled(){
         return this.filled;
     }
     public static int getNumOvals(){
         return Oval.numOvals;
     }
     public void setX1(int in){
         int temp;
         if(in<0){temp=0;}
         else{temp=in;}
         this.x1=temp;
         
     }
     public void setY1(int in){
         int temp;
         if(in<0){temp=0;}
         else{temp=in;}
         this.y1=temp;
     }
     public void setX2(int in){
         int temp;
         if(in<0){temp=0;}
         else{temp=in;}
         this.x2 = temp;
     }
     public void setY2(int in){
         int temp;
         if(in<0){temp=0;}
         else{temp=in;}
         this.y2 = temp;
     }
     public void setFilled(boolean in){
         this.filled = in;
     }
    
    // Returns Upper-left X coordinate for current Oval object
    public int getUpperLeftX() {
        // *** COMPLETE THIS CODE ***
        // Hint: There is a helpful method in the Math class for this
        return Math.min(this.x1,this.x2);
    }
        
    // Returns Upper-left Y coordinate for current Oval object
    // *** CREATE A SIMILAR METHOD FOR getUpperLeftY() HERE ***
    public int getUpperLeftY() {
        // *** COMPLETE THIS CODE ***
        // Hint: There is a helpful method in the Math class for this
        return Math.min(this.y1,this.y2);
    }


    // Returns width in pixels for current Oval object
    public int getWidth() {
        // *** COMPLETE THIS CODE ***
        // Hint: There is a helpful method in the Math class for this
        return Math.max(this.x1,this.x2)-Math.min(this.x1,this.x2);
    }

    // Returns height in pixels for current Oval object
    // *** CREATE A SIMILAR METHOD FOR getHeight() HERE ***
    public int getHeight() {
            // *** COMPLETE THIS CODE ***
            // Hint: There is a helpful method in the Math class for this
            return Math.max(this.y1,this.y2)-Math.min(this.y1,this.y2);
        }
        public boolean isCircle(){
            if(this.getWidth()==this.getHeight()){
                return true;
            }
            return false;
        }

    // Returns the area of the current Oval in pixels
    public double calcArea() {
        // *** COMPLETE THIS CODE ***
        // Hint: Use the getWidth() and getHeight() methods.
        return Math.PI * this.getWidth()/2 * this.getHeight()/2;
    }
    
    // *** DO NOT CHANGE THE CODE BELOW ***
    // Prints the instance variables of the current Oval object
    public String toString() {
        
        return String.format("I am an oval with (x1=%d, y1=%d), (x2=%d, y2=%d), and filled = %b", x1, y1, x2, y2, filled);
    }
}
