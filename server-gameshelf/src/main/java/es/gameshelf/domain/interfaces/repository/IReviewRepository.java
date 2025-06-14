package es.gameshelf.domain.interfaces.repository;

import es.gameshelf.domain.Review;
import es.gameshelf.domain.Game;
import es.gameshelf.domain.User;

import java.util.List;
/**
 * @author Nabil L. A. @nalleon
 */
public interface IReviewRepository {
    Review save(Review review);
    List<Review> findAll();
    Review findById(Integer id);
    List<Review> findAllByUser(User user);
    List<Review> findAllByGame(Game game);
    List<Review> findAllByUserLatest(User user);
    List<Review> findAllByGameLatest(Game game);
    boolean delete(Integer id);
    Review update(Review review);
}
